import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PlayersComponent } from './players.component';

const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component').then(m => m.HomeComponent),
    title: 'Accueil - Espoir Sportif de Chorbane'
  },
  {
    path: 'actualites',
    loadComponent: () => import('./news/news.component').then(m => m.NewsComponent),
    title: 'Actualités - Espoir Sportif de Chorbane'
  },
  {
    path: 'calendrier',
    loadComponent: () => import('./calendar/calendar.component').then(m => m.CalendarComponent),
    title: 'Calendrier - Espoir Sportif de Chorbane'
  },
  {
    path: 'classement',
    loadComponent: () => import('./rankings/rankings.component').then(m => m.RankingsComponent),
    title: 'Classement - Espoir Sportif de Chorbane'
  },
  {
    path: 'equipe',
    component: PlayersComponent,
    title: 'Équipe - Espoir Sportif de Chorbane'
  },
  {
    path: 'partenaires',
    loadComponent: () => import('./partners/partners.component').then(m => m.PartnersComponent),
    title: 'Partenaires - Espoir Sportif de Chorbane'
  },
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule),
    title: 'Administration - Espoir Sportif de Chorbane'
  },
  {
    path: '**',
    redirectTo: '',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }