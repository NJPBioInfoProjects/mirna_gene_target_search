#!/usr/bin/env python3

from flask import Flask, request, render_template
import mariadb

app = Flask(__name__)

def get_connection():
    try:
        conn = mariadb.connect(
            host= '' #host to your database here
            port= , #port to your database here
            user= '', #your username here
            password= ' ',#your password here
            database= 'miRNA' #name of your database here, miRNA in our case
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise

@app.route('/', methods=['GET'])
def search():
    error = None
    results = []
    count = 0
    mirna1 = request.args.get('mirna1', '').strip()
    mirna2 = request.args.get('mirna2', '').strip()
    max_score = request.args.get('max_score', '-0.1').strip()  # default threshold

    # if parameters are provided
    if request.args:
        if not mirna1 or not mirna2:
            error = "Error: Both miRNA names must be entered."
        else:
            try:
                connection = get_connection()
                cursor = connection.cursor()

                # Aggregate errors if miRNA is not found:
                errors = []
                check_query = "SELECT COUNT(*) FROM miRNA WHERE name = ?"

                cursor.execute(check_query, (mirna1,))
                if cursor.fetchone()[0] == 0:
                    errors.append(f"Error in miRNA 1: miRNA '{mirna1}' does not exist in the database.")

                cursor.execute(check_query, (mirna2,))
                if cursor.fetchone()[0] == 0:
                    errors.append(f"Error in miRNA 2: miRNA '{mirna2}' does not exist in the database.")

                if errors:
                    error = "<br>".join(errors)

                if not error:
                    try:
                        max_score_val = float(max_score)
                    except ValueError:
                        error = "Error: Maximum score must be a valid number."

                    if not error:
                        # Build query with dynamic column aliases using old-style % formatting.
                        query = (
                            "SELECT t1.gid, g.name AS gene_name, "
                            "t1.score AS '%s score', t2.score AS '%s score' "
                            "FROM targets t1 "
                            "JOIN targets t2 ON t1.gid = t2.gid "
                            "JOIN miRNA m1 ON t1.mid = m1.mid "
                            "JOIN miRNA m2 ON t2.mid = m2.mid "
                            "JOIN gene g ON g.gid = t1.gid "
                            "WHERE m1.name = %%s AND m2.name = %%s "
                            "AND t1.score IS NOT NULL AND t2.score IS NOT NULL "
                            "AND t1.score <= %%s AND t2.score <= %%s "
                            "ORDER BY (t1.score + t2.score) ASC"
                        ) % (mirna1, mirna2)
                        cursor.execute(query, [mirna1, mirna2, max_score_val, max_score_val])
                        results = cursor.fetchall()
                        count = len(results)
            except Exception as e:
                error = f"Database error: {str(e)}"
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'connection' in locals():
                    connection.close()

    return render_template('nicolaspetrunich_Search.html', 
                           error=error, results=results, count=count, 
                           mirna1=mirna1, mirna2=mirna2, max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True)