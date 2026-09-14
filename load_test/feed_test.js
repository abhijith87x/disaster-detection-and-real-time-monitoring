import http from 'k6/http';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  http.get('http://localhost:8002/feed/reports/latest?cache=false');
}