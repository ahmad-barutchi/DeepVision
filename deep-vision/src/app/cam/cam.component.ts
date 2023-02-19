import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CamService } from './cam.service';

@Component({
  selector: 'app-webcam',
  template: `
    <video #video autoplay></video>
    <canvas #canvas></canvas>
    <button name="file"  type="submit" (click)="startCapture()">Start</button>
    <button (click)="stopCapture()">Stop</button>
  `,
  styles: [`
    video {
      width: 360px;
    }
    canvas {
      display: none;
    }
  `]
})
export class CamComponent {
  @ViewChild('video', { static: true }) video: any;

  @ViewChild('canvas')
  canvas: any;

  private stream: any;
  private requestId: any;
  private sending: boolean = false;

  constructor(private webcamService: CamService) {

  }

  ngAfterViewInit() {
    const videoEl = this.video.nativeElement;
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
      .then((stream: MediaStream) => {
        this.stream = stream;
        videoEl.srcObject = stream;
      })
      .catch((err) => {
        console.error(err);
      });
  }

  startCapture() {
    console.log("startCapture")
    const canvasEl = this.canvas.nativeElement;
    const videoEl = this.video.nativeElement;
    const context = canvasEl.getContext('2d');

    canvasEl.width = videoEl.videoWidth;
    canvasEl.height = videoEl.videoHeight;

    this.requestId = requestAnimationFrame(() => this.captureFrame(canvasEl, context));
  }

  stopCapture() {
    cancelAnimationFrame(this.requestId);
    this.stream.getTracks().forEach((track: { stop: () => void; }) => {
      track.stop();
    });
  }

  captureFrame(canvasEl: HTMLCanvasElement, context: CanvasRenderingContext2D) {
    context.drawImage(this.video.nativeElement, 0, 0, canvasEl.width, canvasEl.height);

    const imageData = canvasEl.toDataURL('image/jpeg', 0.5);

    if (!this.sending) {
      this.sending = true;
      this.webcamService.sendImage(imageData).subscribe(() => {
        this.sending = false;
      });
    }

    this.requestId = requestAnimationFrame(() => this.captureFrame(canvasEl, context));
  }
}
