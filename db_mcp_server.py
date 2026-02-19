import mysql.connector
from mcp.server.fastmcp import FastMCP
from config import DB_CONFIG

mcp = FastMCP("Database Server")

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@mcp.tool()
def get_all_students():
    """Fetch all students from database"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        conn.close()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def get_students_by_department(department: str):
    """Fetch students filtered by department"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM students WHERE department=%s",
            (department,)
        )
        data = cursor.fetchall()
        conn.close()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()

