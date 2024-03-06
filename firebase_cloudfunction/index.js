/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

// const {onRequest} = require("firebase-functions/v2/https");
// const logger = require("firebase-functions/logger");

// Create and deploy your first functions
// https://firebase.google.com/docs/functions/get-started

// exports.helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

const functions = require("firebase-functions");
const admin = require("firebase-admin");
admin.initializeApp();

exports.updateLatestPrediction = functions.database.ref("/predictions/{pushId}")
    .onCreate((snapshot, context) => {
      const newPrediction = snapshot.val();
      // Assuming each prediction has a 'predicted_label'
      const predictedLabel = newPrediction.predicted_label;
      // Update the latestPrediction node
      return admin.database().ref("/latestPrediction").set(predictedLabel);
    });
