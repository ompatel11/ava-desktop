const functions = require('firebase-functions');
// The Firebase Admin SDK to access Firestore.
const admin = require('firebase-admin');
const YAML = require('yaml');

const express = require('express');
const cors = require('cors');
const { auth } = require('firebase-admin');
const { cert } = require('firebase-admin/app');
var serviceAccount = require("/Users/Om/Desktop/ava-desktop/Cloud Functions/functions/secrets/ava-daemon-firebase-adminsdk-q4clz-6e160cc7df.json");
const { firestore } = require('firebase-admin');

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://ava-daemon.firebaseio.com"
});
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
// const config = JSON.parse(process.env.FIREBASE_CONFIG)

// admin.initializeApp(config);

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
    let isBreak = true;
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
