import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <header class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand" href="#">
          <img src="assets/logo.png" alt="ESC Logo" height="40" class="me-2">
          Espoir Sportif de Chorbane
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Accueil</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/actualites" routerLinkActive="active">Actualités</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/calendrier" routerLinkActive="active">Calendrier</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/classement" routerLinkActive="active">Classement</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/equipe" routerLinkActive="active">Équipe</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/partenaires" routerLinkActive="active">Partenaires</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/admin" routerLinkActive="active">Admin</a>
            </li>
          </ul>
        </div>
      </div>
    </header>

    <main class="container py-4">
      <router-outlet></router-outlet>
    </main>

    <footer class="bg-dark text-white py-4 mt-5">
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <h5>Espoir Sportif de Chorbane</h5>
            <p>Club de football fondé en 1980</p>
            <p>Stade Municipal de Chorbane</p>
          </div>
          <div class="col-md-4">
            <h5>Contact</h5>
            <p><i class="bi bi-envelope"></i> contact@esc-football.com</p>
            <p><i class="bi bi-telephone"></i> +216 XX XXX XXX</p>
            <p><i class="bi bi-geo-alt"></i> Chorbane, Tunisie</p>
          </div>
          <div class="col-md-4">
            <h5>Suivez-nous</h5>
            <div class="d-flex gap-3 fs-4">
              <a href="#" class="text-white"><i class="bi bi-facebook"></i></a>
              <a href="#" class="text-white"><i class="bi bi-twitter"></i></a>
              <a href="#" class="text-white"><i class="bi bi-instagram"></i></a>
              <a href="#" class="text-white"><i class="bi bi-youtube"></i></a>
            </div>
          </div>
        </div>
        <hr>
        <div class="text-center">
          <p class="mb-0">&copy; 2023 Espoir Sportif de Chorbane. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  `,
  styles: [`
    .navbar-brand {
      display: flex;
      align-items: center;
    }
    
    .nav-link.active {
      font-weight: bold;
    }
  `]
})
export class AppComponent {
  title = 'Espoir Sportif de Chorbane';
}