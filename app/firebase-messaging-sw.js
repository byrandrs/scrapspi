importScripts('https://www.gstatic.com/firebasejs/8.0.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.0.0/firebase-messaging.js');

// Configura Firebase
var firebaseConfig = {
    apiKey: "AIzaSyB0AlyJHzTZK3QR5o9-9NN3O2-Kuvp3uHk",
    authDomain: "scrap-rnt.firebaseapp.com",
    databaseURL: "https://scrap-rnt-default-rtdb.firebaseio.com",
    projectId: "scrap-rnt",
    storageBucket: "scrap-rnt.appspot.com",
    messagingSenderId: "525166485488",
    appId: "1:525166485488:web:9a86d1d4027bdabdfdc735",
    measurementId: "G-SS0RBSBH09"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// Personaliza el comportamiento de las notificaciones push recibidas
messaging.onBackgroundMessage(function(payload) {
  console.log('Received background message:', payload);

  // Personaliza aquí cómo deseas mostrar la notificación push en segundo plano
  const notificationOptions = {
    body: payload.data.message,
    icon: '/path/to/icon.png'
  };

  self.registration.showNotification(payload.data.title, notificationOptions);
});
