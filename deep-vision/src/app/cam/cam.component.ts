import {   Component,
  NgModule,
  VERSION,
  ViewChild,
  ViewChildren,
  QueryList,
  ElementRef,
  AfterViewInit
} from '@angular/core';

@Component({
  selector: 'app-cam',
  template: `
  <pre *ngIf="error">
            {{error | json}}
          </pre>
  <div class="vid">
    <video #video width="350" height="400"></video>
  </div>
  `,
  styleUrls: ['./cam.component.scss']
})
export class CamComponent implements AfterViewInit {
  title = "live-video-demo";
  @ViewChild("video")
  video: ElementRef<HTMLVideoElement>
  ngVersion: string;
  streaming = false;
  error: any;
  private stream: any = null;
  private constraints = {
    audio: false,
    video: true,
  };

  constructor() {
    this.video = new ElementRef(document.createElement('video'));
    this.ngVersion = `Angular! v${VERSION.full}`;
  }

  ngAfterViewInit() {
    this.initVideo();
  }

  initVideo() {
    this.getMediaStream()
      .then((stream) => {
        this.stream = stream;
        this.streaming = true;
      })
      .catch((err) => {
        this.streaming = false;
        this.error = err.message + " (" + err.name + ":" + err.constraintName + ")";
      });
  }
  private getMediaStream(): Promise<MediaStream> {

    const video_constraints = { video: true };
    const _video = this.video.nativeElement;
    return new Promise<MediaStream>((resolve, reject) => {
      // (get the stream)
      return navigator.mediaDevices.
      getUserMedia(video_constraints)
        .then(stream => {
          (<any>window).stream = stream; // make variable available to browser console
          _video.srcObject = stream;
          // _video.src = window.URL.createObjectURL(stream);
          _video.onloadedmetadata = function (e: any) { };
          _video.play();
          return resolve(stream);
        })
        .catch(err => reject(err));
    });
  }



}
