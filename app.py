from flask import Flask, request, jsonify
from supabase import create_client, Client
import json
from caro_ai import get_best_move
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
POSTGRES_URL = os.getenv("POSTGRES_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# PostgreSQL connection string
engine = create_engine(POSTGRES_URL)

def board_key(board, player, difficulty):
    return json.dumps({"board": board, "player": player, "difficulty": difficulty})

@app.route('/api/caro/move', methods=['POST'])
def get_move():
    data = request.json
    board = data['board']
    player = data['player']
    difficulty = data.get('difficulty', 'medium')
    key = board_key(board, player, difficulty)

    # Check cache
    res = supabase.table('ai_cache').select('move').eq('board', key).execute()
    if res.data:
        move = json.loads(res.data[0]['move'])
        return jsonify(move=move, cached=True)

    # Calculate move
    move = get_best_move(board, player, difficulty)
    # Save to cache
    supabase.table('ai_cache').insert({"board": key, "player": player, "difficulty": difficulty, "move": json.dumps(move)}).execute()
    return jsonify(move=move, cached=False)

@app.route('/api/db/test')
def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
        return jsonify({"status": "success", "version": version})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0') 