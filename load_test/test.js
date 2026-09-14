import http from 'k6/http';

const image = open('./test_image2.jpeg', 'b');

export const options = {
    vus: 200,
    duration: '30s',
};

export default function () {
    const data = {
        file: http.file(image, 'test_image2.jpeg', 'image/jpeg'),
    };

    http.post(
        "http://127.0.0.1:8003/detect/disaster",
        data
    );
}