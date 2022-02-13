'use-scrict';
// const serviceAccountFile = require("../functions/secrets/ava-daemon-firebase-adminsdk-q4clz-6e160cc7df.json")
const functions = require('firebase-functions');
// The Firebase Admin SDK to access Firestore.
const admin = require('firebase-admin');
// var serviceAccount = serviceAccountFile
admin.initializeApp({
    credential: admin.credential.cert({
        "type": "service_account",
        "project_id": "ava-daemon",
        "private_key_id": "6e160cc7dfbce1a24ab83366fc29e12db6020cc0",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDMAThktgdkyXt8\nsfF1wc7edvO8YR7vymTHDtd9NTAdv7qIAEIp6Z0XSE4oLzrLAS2qShg7nX/HAF6p\naMdILBxVHdypMj5A/sU7DIHYEKCslzb8gi4NtXw4qQ00e57Pp6M9Gpp7/aWWkdsf\nyh1GO7hXHOyRr31mnrGC9iFCtpwy6YfiXpysePyrsu+bNabtNmC2/mouGDFEVqPN\nsUN/Lrrt2qfNe6bnPMc1KocoeAIsEzu3DtNFevd8OJcHZ59S5nmyPiMPg6Sa7O7A\nxTS5cxA3SzaP0ZLbKjmqp+Dc52Ts15JwWuOG3RbOjQ++ahEaUkJsX1nGFCAeVC1J\nhOVZYpR5AgMBAAECggEAUcLjcSmrSO+feFhw57snR+3wvb1HAt/hCA6guuPIRwQC\npGNGITop5ZzrBhv3ukjcnnVXxPzYq08woUEHLZvQNyTivUUPwkjZj1Lx70CqxMFO\nHmGmR4RHJwZJ7pDlE2CigejZpXwBE5mdct40YWOp++/xuGnXHnvXtR8kMXKyo4xR\nqBXu9/K8mh46WbEFIKULjio+3HLESye3nIgYoMt4iRcHkzZGxkr29tZsix7JwEE1\nikwLcqNmPKBEiqsDDVnnHI/dmBNg1TvvqXj/Q3fPZylqYqX+bTm7UyXrQLVg90ZF\njZK+x3uvE9k78NU30icapgIl5zyfZYDLGqEKH1nCyQKBgQDwdwsRTUw5P58145MH\nRTgR0v/W152ejHXaityAQUD8R8knrl5v5ZkCA22p2Y119t20FeefnIUJBgZo0Q1G\n2kbNPHFKjDFdp2yva4SjNIsGWeSXUs4QhCRHNxGRrrOoZqKDdPeuogLwE3uANX5K\n2uVv71BojJlnGy247pLWVQQXfwKBgQDZLyzhODYiUx46QRDyBFRZCNt/csQ/vOM8\nHFXkRg5m3eZ0JorXzDFatORN+0ddQkKNlGOr07NG3JZS1I+9Q+zXav3ZbgGWVvc0\nJl2ME3yB33+E0ynmTpnLkvphwEaM25fwFlfguLI+cEp2Y2zFnFGzJxFIRCgHGXy5\nXZ1a0jIQBwKBgGV4ZnQzoRGbVkzALn/n5qQm3IzFSZ7o+KZy6F86qfiLNkgHXZRs\nV2exGKqOwhHgTWe7wpTo0H6hSz0Z0jduzme2tLvXctFpYASaI0tXVb8lWb+9UnVH\nvaNLip9mECvku3krd4T6mrDCF+BfMl7WBfF5E/46LlWC84VRLydAksxzAoGBAIpv\nhZ3xpJ/wdz4Op2x80f8GpFLypqEyF24DacRd22Q6YWD8CFhRccwtrbD/UJfjWmTA\nh1/JS2cJyE/36b9sgpU1P6XOdviLans1UT+uVBi8i53ws653v5SBlVOlqdKzTn/c\n3hsB36vpC6225mh3oaQebOexego8dsH5KAnyHbMVAoGBALBI1Ce8mUCFLrTstn/X\na4aQMm9tIwyzwW+BEAyKMaK5BIkpoLxAJHTbb2NIHOQ6/GlmBmU2ofYKRD0DAbOt\nehaRDtiWVuEjqYlYOt+94Z540eIS1tL3UfaByX0m0Nq0hjxs8P/7pQYG5M/ShfXW\nFT68kqb4K46sUI4kRIhOAmMG\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-q4clz@ava-daemon.iam.gserviceaccount.com",
        "client_id": "112068333216844479414",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-q4clz%40ava-daemon.iam.gserviceaccount.com"
    }),
    databaseURL: "https://ava-daemon.firebaseio.com"
});
const express = require('express');
const cors = require('cors');
const auth = admin.app().auth();
// const { firestore } = require('firebase-admin');
const firestore = admin.firestore();


const db = admin.firestore();
const app = express();

const statusCodes = {
    '100': 'Continue',
    '101': 'Switching Protocols',
    '102': 'Processing',
    '200': 'OK',
    '201': 'Created',
    '202': 'Accepted',
    '203': 'Non-Authoritative Information',
    '204': 'No Content',
    '205': 'Reset Content',
    '206': 'Partial Content',
    '207': 'Multi-Status',
    '300': 'Multiple Choices',
    '301': 'Moved Permanently',
    '302': 'Moved Temporarily',
    '303': 'See Other',
    '304': 'Not Modified',
    '305': 'Use Proxy',
    '307': 'Temporary Redirect',
    '400': 'Bad Request',
    '401': 'Unauthorized',
    '402': 'Payment Required',
    '403': 'Forbidden',
    '404': 'Not Found',
    '405': 'Method Not Allowed',
    '406': 'Not Acceptable',
    '407': 'Proxy Authentication Required',
    '408': 'Request Time-out',
    '409': 'Conflict',
    '410': 'Gone',
    '411': 'Length Required',
    '412': 'Precondition Failed',
    '413': 'Request Entity Too Large',
    '414': 'Request-URI Too Large',
    '415': 'Unsupported Media Type',
    '416': 'Requested Range Not Satisfiable',
    '417': 'Expectation Failed',
    '418': 'I\'m a teapot',
    '422': 'Unprocessable Entity',
    '423': 'Locked',
    '424': 'Failed Dependency',
    '425': 'Unordered Collection',
    '426': 'Upgrade Required',
    '428': 'Precondition Required',
    '429': 'Too Many Requests',
    '431': 'Request Header Fields Too Large',
    '500': 'Internal Server Error',
    '501': 'Not Implemented',
    '502': 'Bad Gateway',
    '503': 'Service Unavailable',
    '504': 'Gateway Time-out',
    '505': 'HTTP Version Not Supported',
    '506': 'Variant Also Negotiates',
    '507': 'Insufficient Storage',
    '509': 'Bandwidth Limit Exceeded',
    '510': 'Not Extended',
    '511': 'Network Authentication Required'
}
// Automatically allow cross-origin requests
app.use(cors({ origin: true }));

app.get("/gettoken", async (req, res) => {

    var bits = 16;
    var len = 28;
    var outStr = "", newStr;
    while (true) {
        while (outStr.length < len) {
            newStr = Math.random().toString(bits).slice(2);
            outStr += newStr.slice(0, Math.min(newStr.length, (len - outStr.length)));
        }
        result = await auth().getUser(outStr)
            .then(() => {
                return false;
            })
            .catch(() => {
                return true;
            })
        if (result === true) {
            // Send the response and break
            break;
        }
    }
    functions.logger.debug(result, { structuredData: true });
    auth().createCustomToken(outStr)
        .then((customToken) => {
            console.log(customToken);
            functions.logger.info("Custom Token generated for " + outStr, { structuredData: true });
            res.send({ "status": 200, "message": statusCodes["200"], "uid": outStr, "customToken": customToken });
        })
        .catch((error) => {
            functions.logger.error(error, { structuredData: true });
            res.send({ "status": 409, "message": statusCodes["409"] });
        })
})

app.get("/settasks", async (req, res) => {
    let tasks = req.query.tasks;
    let uid = req.query.uid;

    functions.logger.debug(tasks, { structuredData: true })
    let putData = await admin.database().ref("users_authenticated").child(uid).set({
        "tasks": tasks
    })
    let data = await admin.database().ref("users_authenticated").child(uid).get();
    // functions.logger.debug(data.val()['tasks'], { structuredData: true })
    res.send(data.val()['tasks']);
})
app.get("/setloginstate", async (req, res) => {

    const email = req.query.email;
    const uid = req.query.uid;
    const authtoken = req.query.authtoken;
    const isverified = req.query.isverified;
    const loginstate = req.query.loginstate;

    try {
        let result = await db.collection("users_authenticated").doc(email).set({
            uid: uid,
            email: email,
            authtoken: authtoken,
            isverified: isverified,
            loginstate: loginstate,
            lastloggedin: firestore.Timestamp.now()
        });
        res.send({ "status": 200, "message": statusCodes["200"] });
    }
    catch (error) {
        res.send({ 'status': 404, "message": statusCodes["404"], "error": error });
    }
})
app.get('/readloginstate', async (req, res) => {
    const email = req.query.email;

    try {
        let result = await db.collection("users_authenticated").doc(email).get();
        functions.logger.debug(result.data(), { structuredData: true });
        if (result.data() !== undefined) {
            functions.logger.debug(result.data())
            res.send({ "status": 200, "message": statusCodes["200"], "data": result.data() });
        }
        else {
            res.send({ 'status': 404, "message": statusCodes["404"] });
        }
    }
    catch (error) {
        res.send({ 'status': 404, "message": statusCodes["404"] });
    }

})
app.get('/verify', (req, res) => {
    const uid = req.query.uid;
    if (uid === undefined) {
        res.send({ "status:": 400, "message": statusCodes[400] })
    }
    functions.logger.debug(uid, { structuredData: true });
    admin.app().auth().listUsers().then((data) => {
        functions.logger.error(data, { structuredData: true });
    })
    admin.app().auth()
        .getUser(uid)
        .then((userRecord) => {
            // See the UserRecord reference doc for the contents of userRecord.
            console.log(`Successfully fetched user data: ${userRecord.toJSON()}`);
            const data = userRecord.toJSON();
            if (data["emailVerified"] == true) {
                isBreak = false;
                // res.send({ "uid": uid, "emailVerified": "True" });
                res.send("Verified")
            }
            else {
                res.send("Not verified")
            }
            // res.send(userRecord.toJSON());
        })
        .catch((error) => {
            console.log('Error fetching user data:', error);
            res.send(error);
        });
});

// Expose Express API as a single Cloud Function:
exports.app = functions.https.onRequest(app);
