import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, HttpClientModule],
  template: `
    <div class="home-container">
      <!-- Hero Section -->
      <section class="hero-section mb-5">
        <div class="row">
          <div class="col-md-6">
            <h1 class="display-4">Bienvenue à l'Espoir Sportif de Chorbane</h1>
            <p class="lead">Club de football tunisien fondé en 1980, l'ESC est fier de représenter la ville de Chorbane dans les compétitions nationales.</p>
            <div class="d-grid gap-2 d-md-flex justify-content-md-start">
              <a routerLink="/equipe" class="btn btn-primary btn-lg px-4 me-md-2">Notre Équipe</a>
              <a routerLink="/calendrier" class="btn btn-outline-secondary btn-lg px-4">Calendrier</a>
            </div>
          </div>
          <div class="col-md-6">
            <img src="assets/stadium.jpg" alt="Stade de Chorbane" class="img-fluid rounded shadow">
          </div>
        </div>
      </section>

      <!-- Next Match Section -->
      <section class="next-match-section mb-5">
        <div class="card border-0 bg-light">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Prochain Match</h2>
            <div class="row align-items-center text-center">
              <div class="col-md-5">
                <img src="assets/logo.png" alt="ESC Logo" height="80">
                <h4 class="mt-2">Espoir Sportif de Chorbane</h4>
              </div>
              <div class="col-md-2">
                <div class="match-info">
                  <h3 class="match-date">15 Juin 2023</h3>
                  <p class="match-time">15:00</p>
                  <span class="badge bg-primary">Championnat</span>
                </div>
              </div>
              <div class="col-md-5">
                <img src="assets/opponent-logo.png" alt="Opponent Logo" height="80">
                <h4 class="mt-2">Club Sportif Rival</h4>
              </div>
            </div>
            <div class="text-center mt-3">
              <a routerLink="/calendrier" class="btn btn-outline-primary">Voir tous les matchs</a>
            </div>
          </div>
        </div>
      </section>

      <!-- Latest News Section -->
      <section class="latest-news-section mb-5">
        <h2 class="mb-4">Dernières Actualités</h2>
        <div class="row">
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <img src="assets/news1.jpg" class="card-img-top" alt="Actualité 1">
              <div class="card-body">
                <h5 class="card-title">Victoire éclatante contre l'équipe rivale</h5>
                <p class="card-text">L'ESC a remporté une victoire impressionnante 3-0 lors du dernier match à domicile.</p>
                <p class="text-muted">10 juin 2023</p>
                <a href="#" class="btn btn-sm btn-primary">Lire plus</a>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <img src="assets/news2.jpg" class="card-img-top" alt="Actualité 2">
              <div class="card-body">
                <h5 class="card-title">Nouveau joueur rejoint l'équipe</h5>
                <p class="card-text">L'attaquant prometteur Ahmed Ben Mohamed a signé un contrat de 3 ans avec l'ESC.</p>
                <p class="text-muted">5 juin 2023</p>
                <a href="#" class="btn btn-sm btn-primary">Lire plus</a>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <img src="assets/news3.jpg" class="card-img-top" alt="Actualité 3">
              <div class="card-body">
                <h5 class="card-title">Rénovation du stade municipal</h5>
                <p class="card-text">Les travaux de rénovation du stade municipal de Chorbane ont commencé cette semaine.</p>
                <p class="text-muted">1 juin 2023</p>
                <a href="#" class="btn btn-sm btn-primary">Lire plus</a>
              </div>
            </div>
          </div>
        </div>
        <div class="text-center mt-3">
          <a routerLink="/actualites" class="btn btn-outline-primary">Toutes les actualités</a>
        </div>
      </section>

      <!-- Team Highlights Section -->
      <section class="team-highlights-section mb-5">
        <h2 class="mb-4">Nos Joueurs Vedettes</h2>
        <div class="row">
          <div class="col-md-3 mb-4" *ngFor="let player of featuredPlayers">
            <div class="card h-100 text-center">
              <img [src]="player.photo_url" class="card-img-top player-img" alt="{{ player.first_name }} {{ player.last_name }}">
              <div class="card-body">
                <h5 class="card-title">{{ player.first_name }} {{ player.last_name }}</h5>
                <p class="card-text">{{ player.position }}</p>
                <p class="card-text"><span class="badge bg-primary">{{ player.jersey_number }}</span></p>
              </div>
            </div>
          </div>
        </div>
        <div class="text-center mt-3">
          <a routerLink="/equipe" class="btn btn-outline-primary">Voir toute l'équipe</a>
        </div>
      </section>

      <!-- Partners Section -->
      <section class="partners-section mb-5">
        <h2 class="mb-4">Nos Partenaires</h2>
        <div class="row align-items-center">
          <div class="col-6 col-md-2 mb-4 text-center" *ngFor="let partner of partners">
            <img [src]="partner.logo_url" alt="{{ partner.name }}" class="img-fluid partner-logo">
          </div>
        </div>
        <div class="text-center mt-3">
          <a routerLink="/partenaires" class="btn btn-outline-primary">Tous nos partenaires</a>
        </div>
      </section>
    </div>
  `,
  styles: [`
    .hero-section {
      padding: 3rem 0;
    }
    
    .player-img {
      height: 200px;
      object-fit: cover;
    }
    
    .partner-logo {
      max-height: 80px;
      filter: grayscale(100%);
      transition: filter 0.3s ease;
    }
    
    .partner-logo:hover {
      filter: grayscale(0%);
    }
  `]
})
export class HomeComponent implements OnInit {
  featuredPlayers = [
    {
      id: 1,
      first_name: 'Mohamed',
      last_name: 'Ben Ali',
      jersey_number: 10,
      position: 'Attaquant',
      photo_url: 'assets/player1.jpg'
    },
    {
      id: 2,
      first_name: 'Ahmed',
      last_name: 'Trabelsi',
      jersey_number: 5,
      position: 'Milieu',
      photo_url: 'assets/player2.jpg'
    },
    {
      id: 3,
      first_name: 'Karim',
      last_name: 'Gharbi',
      jersey_number: 1,
      position: 'Gardien',
      photo_url: 'assets/player3.jpg'
    },
    {
      id: 4,
      first_name: 'Youssef',
      last_name: 'Mejri',
      jersey_number: 4,
      position: 'Défenseur',
      photo_url: 'assets/player4.jpg'
    }
  ];

  partners = [
    { id: 1, name: 'Sponsor 1', logo_url: 'assets/sponsor1.png' },
    { id: 2, name: 'Sponsor 2', logo_url: 'assets/sponsor2.png' },
    { id: 3, name: 'Sponsor 3', logo_url: 'assets/sponsor3.png' },
    { id: 4, name: 'Sponsor 4', logo_url: 'assets/sponsor4.png' },
    { id: 5, name: 'Sponsor 5', logo_url: 'assets/sponsor5.png' },
    { id: 6, name: 'Sponsor 6', logo_url: 'assets/sponsor6.png' }
  ];

  constructor() { }

  ngOnInit(): void {
    // In a real application, we would fetch this data from the API
    // For example:
    // this.playerService.getPlayers().subscribe(players => {
    //   this.featuredPlayers = players.slice(0, 4);
    // });
  }
}