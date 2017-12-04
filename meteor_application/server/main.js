import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
    // MongoDB collections
    // Collection with tweets
    twitterData  = new Mongo.Collection('oneYearData');
    // Collection to hold the labels
    labels = new Mongo.Collection('label');
    // Collection to hold the worker information
    workers = new Mongo.Collection('worker');
    // collection to hold the hit information
    hits = new Mongo.Collection('hit');
    // Collections that contains set of tweets corresponding to active Mechanical Turk HITS
    activeTweets = new Mongo.Collection('activeTweet');
    if(Meteor.isServer) {
        console.log('Server is running.....');

        Meteor.publish('data', function(){
            return activeTweets.find({}, {sort: {fitnessFuncValue:1}});
        });

    }


});

