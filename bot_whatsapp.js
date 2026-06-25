const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

// URL del backend en Python (FastAPI). En producción usaremos variables de entorno.
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000/chat';

// Inicializar el cliente de WhatsApp
// Utilizamos LocalAuth para que la sesión quede guardada y no haya que escanear el QR cada vez
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        // Argumentos necesarios para servidores Linux en la nube
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Generar código QR para escanear
client.on('qr', (qr) => {
    console.log('--- NUEVO CÓDIGO QR ---');
    console.log('Por favor, escanea este código con tu celular (WhatsApp Web):');
    qrcode.generate(qr, { small: true });
});

// Evento: Cliente autenticado correctamente
client.on('authenticated', () => {
    console.log('¡Autenticado con éxito en WhatsApp!');
});

// Evento: Cliente listo y conectado
client.on('ready', () => {
    console.log('¡Cliente de WhatsApp listo y escuchando mensajes!');
});

// Evento: Mensaje recibido
client.on('message', async (msg) => {
    // Evitamos procesar estados o mensajes vacíos
    if (!msg.body || msg.isStatus) return;

    // Solo procesamos mensajes de texto directo (puedes ajustar esto para audios/imágenes si lo deseas a futuro)
    if (msg.type !== 'chat') return;

    try {
        console.log(`\n[WhatsApp] Mensaje recibido de ${msg.from}: ${msg.body}`);

        // Enviar el mensaje a nuestro servidor de FastAPI en Python
        const response = await axios.post(PYTHON_API_URL, {
            message: msg.body,
            sender: msg.from
        });

        const reply = response.data.reply;

        if (reply) {
            console.log(`[Python AI] Respondiendo: ${reply}`);
            // Enviar la respuesta de vuelta por WhatsApp
            await client.sendMessage(msg.from, reply);
        }

    } catch (error) {
        console.error('Error al conectar con el servidor Python:', error.message);
        // Opcional: Avisar al usuario en caso de error interno
        // await client.sendMessage(msg.from, 'Lo siento, estoy experimentando un fallo interno en mi servidor.');
    }
});

// Iniciar el cliente
client.initialize();
