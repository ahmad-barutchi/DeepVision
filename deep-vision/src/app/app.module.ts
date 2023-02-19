import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CamComponent } from './cam/cam.component';
import { HomeComponent } from './home/home.component';
import { OptionComponent } from './option/option.component';
import {HttpClientModule} from "@angular/common/http";
import {CamService} from "./cam/cam.service";

@NgModule({
  declarations: [
    AppComponent,
    CamComponent,
    HomeComponent,
    OptionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [CamService],
  bootstrap: [AppComponent]
})
export class AppModule { }
