import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// @Injectable()
@Injectable({
  providedIn: 'root'
})
export class CamService {

  constructor(private http: HttpClient) {}

  sendImage(imageData: string) {
    console.log("sendImage");
    const body = {
      image: imageData
    };
    return this.http.post('https://548a-138-48-2-20.eu.ngrok.io/video_feed', body);
  }}
