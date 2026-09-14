import http from 'k6/http';

export const options = {
  vus: 300,
  duration: '30s',
};

export default function () {
  for (let i = 1; i <= 10; i++) {
    http.get(`http://localhost:8002/feed/reports/latest?page=${i}`);
  }
}