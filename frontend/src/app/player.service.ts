import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Player } from './player.model';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {
  private apiUrl = `${environment.apiUrl}/players`;

  constructor(private http: HttpClient) { }

  /**
   * Get all players with optional filtering
   * @param category Optional category filter
   * @param teamId Optional team ID filter
   * @returns Observable of Player array
   */
  getPlayers(category?: string, teamId?: number): Observable<Player[]> {
    let params = new HttpParams();
    
    if (category) {
      params = params.set('category', category);
    }
    
    if (teamId) {
      params = params.set('team_id', teamId.toString());
    }
    
    return this.http.get<Player[]>(this.apiUrl, { params });
  }

  /**
   * Get a specific player by ID
   * @param id Player ID
   * @returns Observable of Player
   */
  getPlayer(id: number): Observable<Player> {
    return this.http.get<Player>(`${this.apiUrl}/${id}`);
  }

  /**
   * Create a new player
   * @param player Player data
   * @returns Observable of API response
   */
  createPlayer(player: Player): Observable<{ message: string, player: Player }> {
    return this.http.post<{ message: string, player: Player }>(this.apiUrl, player);
  }

  /**
   * Update an existing player
   * @param id Player ID
   * @param player Updated player data
   * @returns Observable of API response
   */
  updatePlayer(id: number, player: Player): Observable<{ message: string, player: Player }> {
    return this.http.put<{ message: string, player: Player }>(`${this.apiUrl}/${id}`, player);
  }

  /**
   * Delete a player
   * @param id Player ID
   * @returns Observable of API response
   */
  deletePlayer(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiUrl}/${id}`);
  }
}