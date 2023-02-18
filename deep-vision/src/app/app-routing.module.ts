import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {CamComponent} from "./cam/cam.component";
import {HomeComponent} from "./home/home.component";
import {OptionComponent} from "./option/option.component";

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'options', component: OptionComponent },
  {path: 'cam', component: CamComponent},
  { path: '**', redirectTo: '/home' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
