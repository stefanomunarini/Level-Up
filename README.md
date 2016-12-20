# Fifty Points Project Plan

## 1. Team

- 604985 Stefano Munarini
- 427272 Simo Santala
- 597254 Phu Pham

## 2. Goal

In this project, we will build a space ship powered by waste
cooker oil. Helm is string operated.

## 3. Plans

### 3.1. Features and Implementation

#### Basic Functionality and Views

The users of the system will be divided into three groups: administrators, developers and players.
A single user account may be in one or more of these groups at the same time. The users can engage
in following actions:

##### All users

- Authentication (login/logout/signup)
- Profile update

##### Administrators

- Accept developer registration requests
- Deactivate users

##### Developers (Phu)

- Add a game: developers are able to add a game URL to his inventory and then set a price for it.
- Remove, update own games: after uploading games for selling, developer can delete his own games or update them (including price, url and other information)
- Game inventory: developer can see a list of his game from the inventory with numbers related to sale statistics.
- Buy game from other developers: developer can also buy other game developed by other people and play just like a normal player.

##### Players

- Buy games
    - Browse/search games on the store
    - View a game page
        - Buy
        - Contact the seller (email address link) (display if the player has bought the game to prevent spam)
        - Go to seller website
        - Share game
- Play games
    - Browse their own games
    - View a game page
        - Play
        - Share the highscore of the game
        - Contact the seller (email address link)
        - View their own scores
        - View game high scores
        - Go to seller website
        - Share game
- View transaction history

These actions represent the base functionality of the system. As the project develops,
new functionality can be added. The following graph shows a rough sketch of how these
actions can be grouped into views, and what the information architecture and interaction
flow of the system will look like.

![](https://git.niksula.hut.fi/munaris1/wsd_project/raw/master/docs/Views.png)

As can be seen from the graph, many of the views can and should be divided into modular
templates. This will ensure rapid redesign and reduce bugs by removing duplicate code.

#### Authentication and permissions (Stefano)

To authenticate users to the system we will use the Django authentication system (see https://docs.djangoproject.com/en/1.10/topics/auth/). Django provides functionalities to authenticate, signup, login, and logout.

After a set of credentials (username and password) have been verified through the method authenticate, we are able to login a user and create a new session.

We will use either the login_required decorator (for function-based views) or the LoginRequired mixin (for class-based views) to block access to pages which require the user to be authenticated. (see https://docs.djangoproject.com/en/1.10/topics/auth/default/)

Moreover, we will set different permissions to different type of users in order to grant access to reserved pages only to some specific categories of users.

#### Game/service interaction & Save/load and resolution feature (Stefano)

When a user has finished playing a game, a POST request will be sent to the server containing all the information about that particular game. As we structured the database, in particular, we will need to send the score, the game_id, the user_id, and the date. The message for this request will have a messageType of type SCORE.

A user will also be able to pause a game. In this case, a POST request with a message containing a messageType of type SAVE will be sent to the server. The message will also includes information about the state of the game (gameState).

When a user wants to load a previous started game, a POST request will be sent with messageType = LOAD_REQUEST. The server will response with a LOAD messageType or an ERROR if something goes wrong.

Finally, a POST request containing a messageType of type SETTING will be sent every time a game has finished loading and it will contain configuration information (such as layout sizes).

#### 3rd party login (Phu)

There are different django packages to implement 3rd party authentication. After doing some research, we decided to use ‘django-allauth’ package to support 3rd-party authentication. ‘Django-allauth’ supports many popular providers out of the box. In this project, we only use a few of them. Users can login or signup with their facebook, google, openID or github account. In our user collection, we have field call ‘provider’ to indicate if the user was created via local authentication or a 3rd party. All the necessary information of user like email, name, date of birth,... will be stored in our database when the 3rd party successfully authenticate the user. Because the 3rd party provider may not have enough information to fit our user model, user will be able to update the missing information later when they get in our platform. 

#### RESTful API (Stefano)

We will develop a set of RESTful APIs which will be used by external developers to integrate our service in third party applications.

Only registered users will be allowed to use our APIs.

The APIs will require the user to be authenticated before being able to execute any request. Moreover, we will add a mechanism to allow users to execute only 100 requests/day, in order to block bad uses of the service. Every user will be authenticated for 24 hours since its last request.

Our APIs will have the following endpoints:
POST /api/v1/login which allows a user to authenticate in order to use the APIs. The body of the request will be
		
		{
			‘username’: ‘username’,
			‘password’: ‘password'
		}

    	and the response will contain a token to be used for every following request.
GET /api/v1/games?token=THE_TOKEN which will return a list of games in alphabetical order (with a pagination of 20 games in order to maintain a low response time)
GET /api/v1/game?token=THE_TOKEN&search_query=QUERY which will search the database for games containing QUERY in their name or description, and will return all the information of a game and the 10 best scores (if available) for that game.
GET /api/v1/scores?token=THE_TOKEN&game_id=GAME_ID which will return the list of scores for a particular game, ordered by score descending)
POST /api/v1/game which will allow developers to create a new game. The request body will be
{
 ‘token’: THE_TOKEN,
'price': 0.99,
'url': URL,
'Is_public': True,
 ‘icon’: byte_stream,
 ‘name’: ‘game_name’,
 ‘description’: description,
 ‘slug’: ‘slug'
}

#### Responsiveness

The project will implement ZURB Foundation, which provides basic HTML, CSS and JavaScript
functionality, to jump start the development. Foundation is also built for mobile and has
[multiple templates](http://foundation.zurb.com/templates). [An ecommerce](http://foundation.zurb.com/templates-previews-sites-f6/ecommerce.html) template will be
used for this project as the website is mainly about browsing and buying games.


> Foundation is built with HTML, CSS and Javascript, the core components of the Web.
> While Foundation is fairly cutting-edge, we use bulletproof technology like jQuery,
> HTML5 Boilerplate and Normalizr as our baseline. We then layer on top components and
> plugins designed to work well in all of our supported browsers and devices.
> 
> Since Foundation only uses front-end technology, it has no incompatibilities with
> back-end or server technology and has been used with everything from Wordpress and
> Drupal to .Net.

#### Social media sharing (Simo)

We use Open Graph Protocol (https://ogp.me), developed by Facebook and also used by Pinterest, and Twitter Cards (https://dev.twitter.com/cards/overview)
Documentation from different Social Media sites:
https://developers.facebook.com/docs/sharing/webmasters/
https://developers.pinterest.com/docs/rich-pins/overview/
https://developers.google.com/+/web/snippet/
In addition to Open Graph and Twitter cards, we use the share button thingys

### 3.2. Models

![](https://git.niksula.hut.fi/munaris1/wsd_project/raw/master/docs/ER.png)

## 4. Priorities (Stefano)

We will start the implementation of the project from the models. After that, we will implemente the authentication system using Django internal authentication system.
Once the authentication has been completed, we will be ready to start to implement the basic functionalities for all the users (homepage, profile-page). After that we will split the work to implement both the developer and the player functionalities. At this stage we will also implement some unit test in order to guarantee the correct output and business logic for sensible functionalities.

Once the whole implementation is working properly, we will focus on developing RESTful APIs, social media sharing button and third-party signin.

We will finally implement our own game, as well as some admin functionalities.

## 5. Process and Time Schedule (Phu)

To deliver a good product, this project requires a lot of time and commitment from all of our members. To manage time and avoid wasting resources, we follow the following process:

- Design and stick to plan: in the beginning of the project, we discuss and develop a list of features, tasks and a projected schedule to complete the tasks. We use Trello as our project management tool.
- Prioritize the task and focus on the most important ones: Based on the list of tasks and features, we give each task a specific priority point indicating the importance level of the task. The task with highest priority point will be on top of the list and will be implement before other tasks. Additional features and tasks will be marked with low priority and will be considered to be implemented when all basic features are completed.
- Assign tasks for each member: The project timeline will be divided into several sprints. In each sprint, we will assign tasks for each member. At the end of the sprint, we will have a sprint meeting to discuss about what have been completed and what have not. Sprint meeting is also the time when we will be planning the workload of the next sprint.
- Estimate resource availability: 

When and how do we work?

Who does mostly what? 

What deadlines do we have for ourselves? 

Communication and tools for management (Trello, Telegram, Google Drive, Git).

### 5.1. Timetable

Sprint 1, week 51
20.12. Project Plan submission (models defined)
23.12. URL Scheme defined and Django (+ Foundation) installed, project setup
24.12 Models implementation + authentication
Sprint 1.5, Christmas (work if you want to)
Templates (Simo)
Sprint 2, weeks 1 & 2

Sprint 3, week 3 & 4
19.2. Final submission

## 6. Testing

- Unit tests
    - User permissions and authentication
    - URL scheme (response code)
    - APIs (authentication, permissions and output)
- User/manual testing
    - Using the app: try out all the features
    - Validation of html css js
    - Validation of open graph stuff
    - Facebook share button

## 7. Risk Analysis