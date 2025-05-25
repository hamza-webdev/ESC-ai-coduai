import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PlayerService } from './player.service';
import { Player } from './player.model';

@Component({
  selector: 'app-players',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, HttpClientModule],
  template: `
    <div class="container mt-4">
      <h1>Joueurs - Espoir Sportif de Chorbane</h1>
      
      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="form-group">
            <label for="categoryFilter">Catégorie</label>
            <select id="categoryFilter" class="form-control" [(ngModel)]="selectedCategory" (change)="applyFilters()">
              <option value="">Toutes les catégories</option>
              <option value="Seniors">Seniors</option>
              <option value="U19">U19</option>
              <option value="U17">U17</option>
              <option value="U15">U15</option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- Players List -->
      <div class="row">
        <div *ngFor="let player of players" class="col-md-4 mb-4">
          <div class="card">
            <img *ngIf="player.photo_url" [src]="player.photo_url" class="card-img-top" alt="{{ player.first_name }} {{ player.last_name }}">
            <div *ngIf="!player.photo_url" class="card-img-top bg-light d-flex justify-content-center align-items-center" style="height: 200px;">
              <i class="bi bi-person" style="font-size: 5rem;"></i>
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ player.first_name }} {{ player.last_name }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">
                <span class="badge bg-primary me-2">{{ player.position }}</span>
                <span class="badge bg-secondary">{{ player.jersey_number }}</span>
              </h6>
              <p class="card-text">{{ player.nationality }}</p>
              <p class="card-text" *ngIf="player.team">Équipe: {{ player.team.name }}</p>
              <button class="btn btn-primary me-2" (click)="viewPlayerDetails(player)">Détails</button>
              <button *ngIf="isAdmin" class="btn btn-warning me-2" (click)="editPlayer(player)">Modifier</button>
              <button *ngIf="isAdmin" class="btn btn-danger" (click)="deletePlayer(player.id)">Supprimer</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Add Player Button (Admin only) -->
      <div *ngIf="isAdmin" class="row mt-3">
        <div class="col-12">
          <button class="btn btn-success" (click)="showAddPlayerForm()">Ajouter un joueur</button>
        </div>
      </div>
      
      <!-- Add/Edit Player Form (Admin only) -->
      <div *ngIf="isAdmin && showForm" class="row mt-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              {{ editMode ? 'Modifier le joueur' : 'Ajouter un joueur' }}
            </div>
            <div class="card-body">
              <form [formGroup]="playerForm" (ngSubmit)="savePlayer()">
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="firstName">Prénom</label>
                      <input type="text" id="firstName" formControlName="first_name" class="form-control" required>
                      <div *ngIf="playerForm.get('first_name').invalid && playerForm.get('first_name').touched" class="text-danger">
                        Prénom requis
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="lastName">Nom</label>
                      <input type="text" id="lastName" formControlName="last_name" class="form-control" required>
                      <div *ngIf="playerForm.get('last_name').invalid && playerForm.get('last_name').touched" class="text-danger">
                        Nom requis
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-4">
                    <div class="form-group mb-3">
                      <label for="jerseyNumber">Numéro de maillot</label>
                      <input type="number" id="jerseyNumber" formControlName="jersey_number" class="form-control">
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="form-group mb-3">
                      <label for="position">Poste</label>
                      <select id="position" formControlName="position" class="form-control">
                        <option value="goalkeeper">Gardien</option>
                        <option value="defender">Défenseur</option>
                        <option value="midfielder">Milieu</option>
                        <option value="forward">Attaquant</option>
                      </select>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="form-group mb-3">
                      <label for="category">Catégorie</label>
                      <select id="category" formControlName="category" class="form-control">
                        <option value="Seniors">Seniors</option>
                        <option value="U19">U19</option>
                        <option value="U17">U17</option>
                        <option value="U15">U15</option>
                      </select>
                    </div>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="birthDate">Date de naissance</label>
                      <input type="date" id="birthDate" formControlName="birth_date" class="form-control">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="nationality">Nationalité</label>
                      <input type="text" id="nationality" formControlName="nationality" class="form-control">
                    </div>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="height">Taille (cm)</label>
                      <input type="number" id="height" formControlName="height" class="form-control">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="weight">Poids (kg)</label>
                      <input type="number" id="weight" formControlName="weight" class="form-control">
                    </div>
                  </div>
                </div>
                
                <div class="form-group mb-3">
                  <label for="photoUrl">URL de la photo</label>
                  <input type="text" id="photoUrl" formControlName="photo_url" class="form-control">
                </div>
                
                <div class="form-group mb-3">
                  <label for="bio">Biographie</label>
                  <textarea id="bio" formControlName="bio" class="form-control" rows="3"></textarea>
                </div>
                
                <div class="form-group mb-3">
                  <label for="teamId">Équipe</label>
                  <select id="teamId" formControlName="team_id" class="form-control">
                    <option [value]="null">Sélectionner une équipe</option>
                    <option *ngFor="let team of teams" [value]="team.id">{{ team.name }}</option>
                  </select>
                </div>
                
                <div class="form-group">
                  <button type="submit" class="btn btn-primary me-2" [disabled]="playerForm.invalid">Enregistrer</button>
                  <button type="button" class="btn btn-secondary" (click)="cancelForm()">Annuler</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Player Details Modal -->
      <div *ngIf="selectedPlayer" class="modal fade show" tabindex="-1" role="dialog" style="display: block;">
        <div class="modal-dialog modal-lg" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ selectedPlayer.first_name }} {{ selectedPlayer.last_name }}</h5>
              <button type="button" class="btn-close" (click)="closePlayerDetails()"></button>
            </div>
            <div class="modal-body">
              <div class="row">
                <div class="col-md-4">
                  <img *ngIf="selectedPlayer.photo_url" [src]="selectedPlayer.photo_url" class="img-fluid" alt="{{ selectedPlayer.first_name }} {{ selectedPlayer.last_name }}">
                  <div *ngIf="!selectedPlayer.photo_url" class="bg-light d-flex justify-content-center align-items-center" style="height: 200px;">
                    <i class="bi bi-person" style="font-size: 5rem;"></i>
                  </div>
                </div>
                <div class="col-md-8">
                  <h3>Informations</h3>
                  <table class="table">
                    <tbody>
                      <tr>
                        <th>Poste</th>
                        <td>{{ selectedPlayer.position }}</td>
                      </tr>
                      <tr>
                        <th>Numéro</th>
                        <td>{{ selectedPlayer.jersey_number }}</td>
                      </tr>
                      <tr>
                        <th>Date de naissance</th>
                        <td>{{ selectedPlayer.birth_date | date }}</td>
                      </tr>
                      <tr>
                        <th>Nationalité</th>
                        <td>{{ selectedPlayer.nationality }}</td>
                      </tr>
                      <tr>
                        <th>Taille</th>
                        <td>{{ selectedPlayer.height }} cm</td>
                      </tr>
                      <tr>
                        <th>Poids</th>
                        <td>{{ selectedPlayer.weight }} kg</td>
                      </tr>
                      <tr>
                        <th>Catégorie</th>
                        <td>{{ selectedPlayer.category }}</td>
                      </tr>
                      <tr>
                        <th>Équipe</th>
                        <td>{{ selectedPlayer.team?.name }}</td>
                      </tr>
                    </tbody>
                  </table>
                  
                  <h3>Biographie</h3>
                  <p>{{ selectedPlayer.bio || 'Aucune biographie disponible.' }}</p>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" (click)="closePlayerDetails()">Fermer</button>
            </div>
          </div>
        </div>
      </div>
      <div *ngIf="selectedPlayer" class="modal-backdrop fade show"></div>
    </div>
  `,
  styles: [`
    .card-img-top {
      height: 200px;
      object-fit: cover;
    }
    
    .modal {
      background-color: rgba(0, 0, 0, 0.5);
    }
  `]
})
export class PlayersComponent implements OnInit {
  players: Player[] = [];
  teams: any[] = [];
  selectedCategory: string = '';
  isAdmin: boolean = false;
  showForm: boolean = false;
  editMode: boolean = false;
  selectedPlayer: Player | null = null;
  playerForm: FormGroup;
  
  constructor(
    private playerService: PlayerService,
    private fb: FormBuilder
  ) {
    this.playerForm = this.fb.group({
      id: [null],
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      jersey_number: [null],
      position: [''],
      birth_date: [null],
      nationality: [''],
      photo_url: [''],
      bio: [''],
      height: [null],
      weight: [null],
      team_id: [null],
      category: ['Seniors']
    });
  }
  
  ngOnInit(): void {
    this.loadPlayers();
    // TODO: Load teams from API
    this.teams = [
      { id: 1, name: 'Espoir Sportif de Chorbane' }
    ];
    
    // TODO: Check if user is admin
    this.isAdmin = false;
  }
  
  loadPlayers(): void {
    this.playerService.getPlayers(this.selectedCategory).subscribe(
      (data) => {
        this.players = data;
      },
      (error) => {
        console.error('Error loading players:', error);
      }
    );
  }
  
  applyFilters(): void {
    this.loadPlayers();
  }
  
  viewPlayerDetails(player: Player): void {
    this.selectedPlayer = player;
  }
  
  closePlayerDetails(): void {
    this.selectedPlayer = null;
  }
  
  showAddPlayerForm(): void {
    this.editMode = false;
    this.playerForm.reset();
    this.playerForm.patchValue({ category: 'Seniors' });
    this.showForm = true;
  }
  
  editPlayer(player: Player): void {
    this.editMode = true;
    this.playerForm.patchValue(player);
    this.showForm = true;
  }
  
  cancelForm(): void {
    this.showForm = false;
  }
  
  savePlayer(): void {
    if (this.playerForm.invalid) {
      return;
    }
    
    const playerData = this.playerForm.value;
    
    if (this.editMode) {
      const playerId = playerData.id;
      this.playerService.updatePlayer(playerId, playerData).subscribe(
        (response) => {
          console.log('Player updated:', response);
          this.showForm = false;
          this.loadPlayers();
        },
        (error) => {
          console.error('Error updating player:', error);
        }
      );
    } else {
      this.playerService.createPlayer(playerData).subscribe(
        (response) => {
          console.log('Player created:', response);
          this.showForm = false;
          this.loadPlayers();
        },
        (error) => {
          console.error('Error creating player:', error);
        }
      );
    }
  }
  
  deletePlayer(id: number): void {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce joueur ?')) {
      this.playerService.deletePlayer(id).subscribe(
        (response) => {
          console.log('Player deleted:', response);
          this.loadPlayers();
        },
        (error) => {
          console.error('Error deleting player:', error);
        }
      );
    }
  }
}