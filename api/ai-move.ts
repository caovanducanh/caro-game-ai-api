import type { VercelRequest, VercelResponse } from '@vercel/node';
import { createClient } from '@supabase/supabase-js';

// Simple AI logic: chọn ô trống đầu tiên (có thể nâng cấp thuật toán sau)
function getBestMove(board: any[][], player: string, difficulty: string) {
  for (let r = 0; r < board.length; r++) {
    for (let c = 0; c < board[r].length; c++) {
      if (!board[r][c]) {
        return { row: r, col: c };
      }
    }
  }
  return null;
}

const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_KEY!);

export default function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const { board, player, difficulty } = req.body;
  if (!board || !player) {
    return res.status(400).json({ error: 'Missing board or player' });
  }
  const move = getBestMove(board, player, difficulty || 'medium');
  if (move) {
    await supabase.from('ai_cache').insert([
      { board: JSON.stringify(board), player, difficulty, move: JSON.stringify(move) }
    ]);
  }
  res.status(200).json({ move });
} 