import { Template } from 'meteor/templating';

import './main.html';

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


q3Options = ['getting_hiredjob_seeking', 'getting_fired', 'quitting_a_job', 'losing_job_some_other_way',
    'getting_promotedraised', 'getting_cut_in_hours', 'complaining_about_work', 'offering_support',
    'going_to_work', 'coming_home_from_work', 'none_of_the_above_but_jobrelated', 'not_jobrelated'];
tweetIDList = [];

workerID = "";
hitID = "";
assignmentID ="";
_id = "";

// List of tweets corresponding to the HIT
tweetList = [];
NUMBER_OF_TWEETS_IN_HIT = 1000; // Just a random number and will be replaced by actually number of tweets.
isShuffled = false;
url = "";

if(Meteor.isClient){
    var count = 0;
    var isComplete = false;

    //console.log("Client");
    Session.set('selectedTweet', -1);
    Session.set('q1', false);
    Session.set('q2', false);
    Session.set('q3', false);

    Template.content.onCreated( function() {
        this.subscribe( 'data', function() {
            $( ".loader" ).delay( 1 ).fadeOut( 'slow', function() {
                $( ".loading-wrapper" ).fadeIn( 'slow' );
            });
        });
    });


    Template.content.onRendered( function() {
        $( "svg" ).delay( 1000 ).fadeIn();
    });


    Template.content.helpers( {

        // Checks whether worker has accepted the HIT
        'validated': function () {
            function turkGetParam( name ) {
                var regexS = "[\?&]"+name+"=([^&#]*)";
                var regex = new RegExp( regexS );
                var tmpURL = fullurl;
                var results = regex.exec( tmpURL );
                if( results === null ) {
                    return "";
                } else {
                    return results[1];
                }
            }

            function insertWorkerInfo() {
                workers.insert({
                    workerID: workerID,
                    assignmentID: assignmentID,
                    hitID: hitID
                });
            }


            // Capture the URL
            var fullurl = window.location.href;

            assignmentID = turkGetParam('assignmentId');
            hitID = turkGetParam('hitId');
            workerID = turkGetParam('workerId');

            console.log(assignmentID);
            console.log(hitID);
            console.log(workerID);
            if(assignmentID !== "ASSIGNMENT_ID_NOT_AVAILABLE" && assignmentID !== "") {
                insertWorkerInfo();
                var turkToSubmit = turkGetParam('turkSubmitTo');
                if (turkToSubmit.indexOf("sandbox") > -1) {
                    url = 'https://workersandbox.mturk.com/mturk/externalSubmit'
                }
                else {
                    url = 'https://www.mturk.com/mturk/externalSubmit'
                }
            }
            return !(workerID === "" || assignmentID === "ASSIGNMENT_ID_NOT_AVAILABLE");

        },

        // Method to fetch the tweets in order
        'document': function () {

            function shuffle(a) {
                var j, x, i;
                for (i = a.length - 1; i > 0; i--) {
                    j = Math.floor(Math.random() * (i + 1));
                    x = a[i];
                    a[i] = a[j];
                    a[j] = x;
                }
            }


            if(Session.get('selectedTweet') === -1) {
                var data = activeTweets.find({'hitID': hitID}).fetch();
                _id = data[0]['_id'];
                tweetList = data[0]['tweets'];
                NUMBER_OF_TWEETS_IN_HIT = tweetList.length;
                if(!isShuffled) {
                    shuffle(tweetList);
                    //console.log(tweetList);
                    activeTweets.update({'_id': _id}, {
                        $set: { tweets: tweetList },
                    });
                    isShuffled = true;
                }

                return tweetList[count];
            }
            else {
                return tweetList[Session.get('selectedTweet')];

            }

        },

        'tweetNumber':function () {
            if (Session.get('selectedTweet') === -1){
                return Session.get('selectedTweet') + 2;
            }
            return Session.get('selectedTweet') + 1;
        },


        'backButton': function () {
            return Session.get('q1') && Session.get('q2') && Session.get('q3');
        },

        // Method to store the HIT info and list of tweet IDs labeled in the corresponding HIT
        'completed': function () {
            if(Session.get('selectedTweet') === NUMBER_OF_TWEETS_IN_HIT) {
                isComplete = true;
                // Inserts list of tweets labeled for an  assignment at the end of a HIT
                // Comment lines 236-241 before uncommenting this.
                hits.insert({
                    hitID: hitID,
                    assignmentID: assignmentID,
                    workerID: workerID,
                    tweetList: tweetIDList
                });
            }
            return isComplete;
        }
    });


    Template.content.events( {
        'click .next': function (event, template) {
            var element1 = template.find('input:radio[name=q1]:checked');
            var element2 = template.find('input:radio[name=q2]:checked');
            var element3 = template.findAll('input:checkbox[name=q3]:checked');
            console.log("Selected options: " + $(element1).val() + " and " + $(element2).val() +
                " and " + $(element3).val());
            Session.set('selectedTweet',  count);
            Session.set('q1', false);
            Session.set('q2', false);
            Session.set('q3', false);


            var selectedBoxes = _.map(element3, function(item) {
                return item.defaultValue;
            });
            //console.log(selectedBoxes.length);

            function isChecked(selectedBoxes, q3Options, index) {
                for(var i=0; i<selectedBoxes.length; i++) {
                    if(selectedBoxes[i] === q3Options[index]) {
                        return 1;
                    }
                }
                return -1;
            }

            var checkboxResult = [];

            for(var idx=0; idx<q3Options.length; idx++) {
                var result = isChecked(selectedBoxes, q3Options, idx);
                checkboxResult.push({'option':q3Options[idx], 'checked': result});
            }


            console.log(checkboxResult);

            var indx = Session.get('selectedTweet');

            var data = tweetList[indx];
            var tweetID = data['id'];
            // var tweetText = data['text'];
            //console.log(data);
            tweetIDList.push(tweetID);

            labels.insert({
                    id: tweetID,
                    timestamp: new Date(),
                    workerID: workerID,
                    assignmentID: assignmentID,
                    hitID: hitID,
                    question1: $(element1).val(),
                    question2: $(element2).val(),
                    question3: checkboxResult
                }
            );

            count += 1;
            Session.set('selectedTweet',  count);

            if(Session.get('selectedTweet') === NUMBER_OF_TWEETS_IN_HIT) {
                // Inserts list of tweets labeled for an  assignment at the end of a HIT
                // Comment lines 160-165 before uncommenting this.
                // This insertion might cause failure of document insertion in label collection
                //hits.insert( {
                    //hitID: hitID,
                    //assignmentID: assignmentID,
                    //workerID: workerID,
                    //tweetList: tweetIDList
                //});
                template.find("form").submit();
            }
            template.find("form").reset();

        },

        /*
        'click .back': function (event, template) {
            count -= 1;
            Session.set('selectedTweet',  count);
            console.log(Session.get('selectedTweet'));
        }
        */
    });


    Template.QandA.helpers( {

        // Method to return assignment ID
        'assignmentID': function () {
            return assignmentID;

        },

        'url': function () {
            return url;
        }
    });

    Template.QandA.events({

        'change .qa': function (event, template) {

            var element1 = template.find('input:radio[name=q1]:checked');
            var element2 = template.find('input:radio[name=q2]:checked');
            var element3 = template.find('input:checkbox[name=q3]:checked');
            /*console.log("Selected options: " + $(element1).val() + " and " + $(element2).val() +
                " and " + $(element3).val()); */

            if($(element1).val() !== undefined) {
                Session.set('q1',  true);
            }

            if($(element2).val() !== undefined) {
                Session.set('q2',  true);
            }

            if($(element3).val() !== undefined) {
                Session.set('q3',  true);
            }

            if($(element3).val() === undefined) {
                Session.set('q3', false);
            }
        }


    });
}




