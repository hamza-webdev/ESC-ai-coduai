/**
 * Interface representing a Player entity
 */
export interface Player {
  id?: number;
  first_name: string;
  last_name: string;
  jersey_number?: number;
  position?: 'goalkeeper' | 'defender' | 'midfielder' | 'forward';
  birth_date?: string;
  nationality?: string;
  photo_url?: string;
  bio?: string;
  height?: number;
  weight?: number;
  team_id?: number;
  category?: string;
  created_at?: string;
  updated_at?: string;
  team?: {
    id: number;
    name: string;
    logo_url?: string;
  };
}

/**
 * Interface for player statistics in a match
 */
export interface PlayerMatchStats {
  player_id: number;
  match_id: number;
  goals: number;
  assists: number;
  yellow_cards: number;
  red_cards: number;
  minutes_played: number;
}