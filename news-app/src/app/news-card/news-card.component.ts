import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-news-card',
  templateUrl: './news-card.component.html',
  styleUrls: ['./news-card.component.css']
})
export class NewsCardComponent {
  @Input() title: string = 'News Title';
  @Input() description: string = 'This is a short description of the news article.';
  @Input() trustScore: number = 0;  // Placeholder for Trust Score
  @Input() biasScore: number = 0;   // Placeholder for Bias Score
  @Input() category: string = 'Category';

  readMore() {
    // Logic for reading more (could be routing or expanding the card)
  }
}
