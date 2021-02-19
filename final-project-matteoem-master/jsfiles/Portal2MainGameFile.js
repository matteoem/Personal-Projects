Physijs.scripts.worker = 'physijs_worker.js';
Physijs.scripts.ammo = 'ammo.js';


var scene, renderer, meshRed,meshBlue,meshYellow,NewmeshRed,NewmeshYellow,NewmeshBlue,soffitto,pavimento;
var meshFloor, ambientLight, light;


ambientLight = new THREE.AmbientLight(0xffffff, 0.8);


var stanza;
var cub = new THREE.Object3D();
var keyboard = {};


var raycaster = new THREE.Raycaster();
var raycaster1 = new THREE.Raycaster();
var raycasterE = new THREE.Raycaster();
var wheatley = new THREE.Object3D();


var stairstep1 = new THREE.Object3D();
var stairstep2 = new THREE.Object3D();
var stairstep3 = new THREE.Object3D();
var stairstep4 = new THREE.Object3D();
var panel =  new THREE.Object3D();


var portal_cube,boundingBoxButton,boundingBoxButton2,boundingBoxButton3,boundingBoxfloor, metaldoor;
var bodyCapsule = new THREE.Object3D();
var upperSphereL = new THREE.Object3D();
var upperSphereR = new THREE.Object3D();
var upperLegL = new THREE.Object3D();
var upperLegR = new THREE.Object3D();
var floatingEye = new THREE.Object3D();
var LowerSphereL = new THREE.Object3D();
var LowerSphereR = new THREE.Object3D();
var LowerLegL = new THREE.Object3D();
var LowerLegR = new THREE.Object3D();
var feetR = new THREE.Object3D();
var feetL = new THREE.Object3D();
var TopButton = new THREE.Object3D();

var radio = new THREE.Object3D();

var dirLight;
var dirLight = new THREE.DirectionalLight(0xc0cfc0, 0.7);

var moveForwardBackward = 0;
var moveLeftRight = 0;
var forceInt = 20;
var moveLR = 0;
var MoveforBack = 0;
var UpDown = 0;
var scalePlus = 0;
var scaleMinus = 0;
var switchingScale = 0;
var turnOnOffLight = true;
var findObject = false;
var removebuttons = new THREE.Object3D();

var target = new THREE.Vector3;
var grabbed = false;
var grabObj;

var column = new THREE.Object3D();

var backgroundMusic = document.getElementById("BackgroundMusic");
var boundingBoxCube = new THREE.Object3D();
var boundingBoxCube2 = new THREE.Object3D();
var boundingBoxCube3 = new THREE.Object3D();

var spotLight = new THREE.SpotLight( 0xffff00,1 );
var spotLight1 = new THREE.SpotLight( 0xffff00,1 );


const geometry = new THREE.BoxBufferGeometry();
const material = new THREE.MeshPhongMaterial({color:0xfffc00});
var clock = new THREE.Clock();
//var delta = clock.getDelta();
const windowHalf = new THREE.Vector2( (window.innerWidth*0.9) / 2, (window.innerHeight*0.9) / 2 );




var updateCharacter = true;
var cake;

var BluePortal;
var OrangePortal;
var blue_active = false;
var orange_active = false;
var InclinedPanels = new THREE.Object3D();
var fps;
var videoTexture;

var targetSpot1;

var anim_state;

var pressed = false;
var pressed2 = false;
var pressed3 = false;

var radio;// = new THREE.Object3D();

var timerdoor = 0;
var alphadoor = 0;

var cubeMerge = new THREE.Object3D();
var testRoom = new THREE.Object3D();

var manager = new THREE.LoadingManager();

manager.onStart = function ( url, itemsLoaded, itemsTotal ) {
};

manager.onLoad = function ( ) {


	CameraLoader();
};


// create an AudioListener and add it to the camera
var listener = new THREE.AudioListener();
var sound = new THREE.Audio( listener );
var ending = new THREE.Audio( listener );
var RadioMusic = new THREE.PositionalAudio( listener );
var portalGunSound = new THREE.Audio( listener );

var audioLoader = new THREE.AudioLoader(manager);

let loader = new THREE.GLTFLoader(manager);
var textureEnding = new THREE.TextureLoader().load( 'media/endingpictv.png' );



function init(){

	document.getElementById("schermata_caricamento").style.display = "block";
	document.getElementById("MenuMacro").style.display = "none";
	document.getElementById("Menu").display = "none";

	


	// Ask the browser to release the pointer
	document.exitPointerLock = document.exitPointerLock ||
	document.mozExitPointerLock ||
	document.webkitExitPointerLock;
	document.exitPointerLock();
	
	//scene = new THREE.Scene();
	
	scene = new Physijs.Scene({reportsize:200, fixedTimeStep:1/60});
	
	scene.setGravity(new THREE.Vector3(0,-10,0));
	
	
	CreateCharacter(document,scene,40,window.innerWidth/window.innerHeight,0.1,10000);
	character.camera.position.set(-23.2,28.35,0.7)
	//character.height=4;
	AddPhysicBody(scene);
	AddIgnoreTag("portal");
	


	
	character.camera.add( listener );
	Lock();

	// load a sound and set it as the PositionalAudio object's buffer
	audioLoader.load( 'media/Portal Radio Tune.mp3', function( buffer ) {
	RadioMusic.setBuffer( buffer );
	RadioMusic.setRefDistance( 5 );
	RadioMusic.setVolume( 0.2 );
	RadioMusic.setLoop( true );
	RadioMusic.play();
	});

	audioLoader.load( 'media/Portal - Still Alive.mp3', function( buffer ) {
		ending.setBuffer( buffer );
		ending.setVolume( 0.6 );
		ending.autoplay=false;
		});

	audioLoader.load( 'Portal gun Shooting Sound Effect.mp3', function( buffer ) {
	//portalGunSound = sound;
	portalGunSound.setBuffer( buffer );
	portalGunSound.setVolume( 0.2 );
	});
	Println(portalGunSound);

	renderer = new THREE.WebGLRenderer({antialias:true});
	renderer.setSize(window.innerWidth,window.innerHeight);
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.PCFSoftShadowMap;
	renderer.shadowMapSoft = true;
	
	onResize();
	
	document.body.appendChild(renderer.domElement);

	
	document.addEventListener( 'mousedown', onDocumentMouseDown, false );
	document.addEventListener('keydown', onKeyDown, false);
	document.addEventListener('keyup', onKeyUp,false);
	$(function() {
		$(window).resize(onResize).trigger('resize');
	  });
	

//#region 
	/*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ */
	
	meshRed = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), new THREE.MeshPhongMaterial({color:0xffffff}), 0);	
	meshRed.receiveShadow = true;
	meshRed.castShadow = true;
	meshRed.rotation.set(0,Math.PI,0);
	meshRed.position.set(43.88,21.87,55.87);		
	meshRed.scale.set(38.88,58.79,156.72);
	scene.add(meshRed);
	meshRed.layers.enable(1);


	NewmeshRed = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), new THREE.MeshPhongMaterial({color:0xffffff}), 0);	
	NewmeshRed.receiveShadow = true;
	NewmeshRed.castShadow = true;
	NewmeshRed.rotation.set(0,Math.PI,0);
	NewmeshRed.position.set(-43.88,21.87,50.87);		
	NewmeshRed.scale.set(32.68,58.79,156.72);
	scene.add(NewmeshRed);
	NewmeshRed.layers.enable(1);

	soffitto = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), new THREE.MeshPhongMaterial({color:0xffffff}), 0);	
	soffitto.receiveShadow = true;
	soffitto.castShadow = true;
	soffitto.rotation.set(0,0,0);
	soffitto.position.set(0,300,0);		
	soffitto.scale.set(101,498,100);
	scene.add(soffitto);
	soffitto.layers.enable(1);



	meshYellow = new Physijs.BoxMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshPhongMaterial({color:0xffffff}),0);
	// The cube can have shadows cast onto it, and it can cast shadows
	meshYellow.receiveShadow = true;
	meshYellow.castShadow = true;
	meshYellow.rotation.set(0,Math.PI*0.5,0);
	meshYellow.position.set(-15.08,21.87,-29.92);		
	meshYellow.scale.set(14.77,58.49,39.43);
	scene.add(meshYellow);
	meshYellow.layers.enable(1);


	NewmeshYellow = new Physijs.BoxMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshPhongMaterial({color:0xffffff}),0);
	// The cube can have shadows cast onto it, and it can cast shadows
	NewmeshYellow.receiveShadow = true;
	NewmeshYellow.castShadow = true;
	NewmeshYellow.rotation.set(0,Math.PI*0.5,0);
	NewmeshYellow.position.set(-15.08,21.87,22.87);		
	NewmeshYellow.scale.set(10.48,58.49,35.13);
	scene.add(NewmeshYellow);
	NewmeshYellow.layers.enable(1);



	meshBlue = new Physijs.BoxMesh(
		new THREE.BoxGeometry(1,1,1),
		new THREE.MeshPhongMaterial({color:0xffffff}), 0
	);
	// The cube can have shadows cast onto it, and it can cast shadows
	meshBlue.receiveShadow = true;
	meshBlue.castShadow = true;
	meshBlue.position.set(12.64,21.87,28.040);
	meshBlue.rotation.set(0,Math.PI*0.5,0);
	meshBlue.scale.set(12.18,58.8,31.01);		
	scene.add(meshBlue);
	meshBlue.layers.enable(1);

		
	NewmeshBlue = new Physijs.BoxMesh(
		new THREE.BoxGeometry(1,1,1),
		new THREE.MeshPhongMaterial({color:0xffffff}), 0
	);
	// The cube can have shadows cast onto it, and it can cast shadows
	NewmeshBlue.receiveShadow = true;
	NewmeshBlue.castShadow = true;
	NewmeshBlue.position.set(19.54,21.87,-28.040);
	NewmeshBlue.rotation.set(0,Math.PI*0.5,0);
	NewmeshBlue.scale.set(27.08,60.6,30.41);		
	scene.add(NewmeshBlue);
	NewmeshBlue.layers.enable(1);

	/*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ */	
//#endregion


	
	
	//#region // LIGHTS
	scene.add(ambientLight);
	
	 dirLight.position.set(24,40,-25);
	dirLight.rotation.set(Math.PI*0.5,0,0);
	dirLight.castShadow = true;
	scene.add(dirLight);
	
	spotLight1.castShadow = true;
	spotLight1.shadow.camera.near = 0;
	spotLight1.shadow.camera.far = 5;
	spotLight1.shadow.camera.fov = 10;
	spotLight1.angle = Math.PI/7;
	spotLight1.distance = 13;
	//spotLight1.angle = Math.PI/12;
	//scene.add( spotLight1 );
	spotLight1.position.set(-0.36,20,7.09)
	targetSpot1 = new THREE.Object3D();
	targetSpot1.position.set(0.36,17,5.39);
	spotLight.target = targetSpot1;

	//#endregion
	
	var materialButton= Physijs.createMaterial(
		new THREE.MeshPhongMaterial({color:0xffff00,  wireframe:true}),
		1
	);
	
	boundingBoxButton = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1),materialButton, 0 );
	boundingBoxButton.receiveShadow = true;
	boundingBoxButton.castShadow = true;
//	boundingBoxButton.scale.set(2,0.3,2);

	boundingBoxButton2 = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), materialButton, 0 );
	boundingBoxButton2.receiveShadow = true;
	boundingBoxButton2.castShadow = true;

	boundingBoxButton3 = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1),materialButton, 0 );
	boundingBoxButton3.receiveShadow = true;
	boundingBoxButton3.castShadow = true;
		
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	
	portalGeometry = new THREE.CircleBufferGeometry(1,32);
	var portalGeom = [portalGeometry,portalGeometry]
	
	CreatePortals(2,scene,40,window.innerWidth*1.11/window.innerHeight,0.1,10000,window.innerWidth,window.innerHeight,portalGeom, new THREE.Vector3(1.45, 2, 1));
	AddCollisionListener(PortalCollisionData, PortalCollision);
	
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


	
	//#region IMPORT DEI MODELLI
	
	loader.load('models/portal_2_test_room/scene.gltf', function(gltf){
		
		//testRoom = gltf.scene.children[0];
		testRoom = gltf.scene;
		testRoom.traverse( function ( child ) {
			
			if ( child instanceof THREE.Mesh ) {	
				child.castShadow = true;
				child.receiveShadow = true;	
				child.layers.enable(1);

			}
			
		});
		
	 	//console.log(dumpObject(testRoom).join('\n'));
		testRoom.rotation.set(0,0,0);
		testRoom.scale.set(5,5,5);

		removeswitch = testRoom.getObjectByName("Switch",true);
		removecubes = testRoom.getObjectByName("Cubes",true);
		removePortalB = testRoom.getObjectByName("Portal_blue",true);
		removePortalO = testRoom.getObjectByName("Portal_orange",true);
		removeWater = testRoom.getObjectByName("Water",true);
		stairstep1 = testRoom.getObjectByName("grid2b000_0",true);
		stairstep2 = testRoom.getObjectByName("grid2b002_0",true);
		stairstep3 = testRoom.getObjectByName("grid2b003_0",true);
		stairstep4 = testRoom.getObjectByName("grid2b001_0",true);
		bottomFloorButton =  testRoom.getObjectByName("Pressure_button",true);


		panel = testRoom.getObjectByName("grid1_0",true);
		column = testRoom.getObjectByName("Cylinder004",true);

		
		stairstep1.rotation.set( 12.4, 18.7, 126.01);
		stairstep2.rotation.set(12.4, 18.7, 126.01)
		stairstep3.rotation.set( 12.4, 18.7, 126.01)
		stairstep4.rotation.set( 12.4, 18.7, 126.01)

		stairstep1.position.set( stairstep1.position.x, stairstep1.position.y, stairstep1.position.z + 0.05);
		stairstep2.position.set(stairstep2.position.x, stairstep2.position.y, stairstep2.position.z + 0.05)
		stairstep3.position.set( stairstep3.position.x, stairstep3.position.y, stairstep3.position.z + 0.05)
		stairstep4.position.set(stairstep4.position.x, stairstep4.position.y, stairstep4.position.z + 0.05)

		removeswitch.position.set(1000,10001,1000);
		removecubes.position.set(1000,10001,1000);
		removePortalB.position.set(1000,10001,1000);
		removePortalO.position.set(1000,10001,1000);
		removeWater.position.set(1000,10001,1000);
		panel.position.set(1000,10001,1000);
		column.position.set(1000,10001,1000);
		
		
		bottomFloorButton.position.set(3.0,-3.95,-6.698);
		bottomFloorButton.scale.set(0.8,0.8,0.8);

		scene.add(testRoom);
		
		testRoom.layers.enable(1);
		
	
		
		boundingBoxButton.material.visible = true;
		boundingBoxButton.scale.set(2*1.5,0.1,2*1.5);
		boundingBoxButton.position.set(-4.92,20.625,-15.009);
		boundingBoxButton.__dirtyPosition = true;
		scene.add(boundingBoxButton);
		boundingBoxButton.material.visible = false;

		boundingBoxButton.layers.enable(1);


		boundingBoxButton2.position.set(-5.1 , 5.45, 5.3);
		boundingBoxButton2.scale.set(2*1,0.3*2 - 0.5,2*1);
		boundingBoxButton2.material.visible = false;
		scene.add(boundingBoxButton2);
		boundingBoxButton2.layers.enable(1);

		boundingBoxButton3.position.set(19.99,35.5,19.6);
		boundingBoxButton3.scale.set(2*0.9, 0.3*1.8 - 0.5, 2*0.9);
		boundingBoxButton3.material.visible = false;
		boundingBoxButton3.layers.enable(1);
		scene.add(boundingBoxButton3);
		p1_outline = testRoom.getObjectByName( "Portal_blue", true );
        p2_outline = testRoom.getObjectByName( "Portal_orange", true );

        portals[0].mesh.add(p1_outline);
        p1_outline.position.set(0,0,-0.01);
        p1_outline.scale.set(1.1,1.1,1.1);
        RegisterActivationCallback(function(){ p1_outline.children[0].name = "portal"; }, portals[0]);

        portals[1].mesh.add(p2_outline);
        p2_outline.position.set(0,0,-0.01);
        p2_outline.scale.set(1.1,1.1,1.1);
        RegisterActivationCallback(function(){ p2_outline.children[0].name = "portal"; }, portals[1]);


	});
	
	loader.load('models/portal_2_test_room/scene.gltf', function(gltf){
		
		//testRoom = gltf.scene.children[0];
		testRoom1 = gltf.scene;
		testRoom1.traverse( function ( child ) {
			
			if ( child instanceof THREE.Mesh ) {	
				child.castShadow = true;
				child.receiveShadow = true;	
				child.layers.enable(1);

			}
			
		});
		
	 	//console.log(dumpObject(testRoom).join('\n'));
		testRoom1.scale.set(5,5,5);

		testRoom1.layers.enable(1);

		TopButton =  testRoom1.getObjectByName("Pressure_button",true);
		scene.add(TopButton);
		TopButton.position.set(19.93, 35, 19.6);
		TopButton.rotation.x -= Math.PI*0.5;
		TopButton.scale.set(1.3,1.3,1.3);



	});



	loader.load('models/TV/scene.gltf', function(gltf){
		tv = gltf.scene.children[0]; //figlio della scena
		tv.castShadow = true;
		// portalGun.scale.set(0.01,0.01,0.01)
		tv.position.set(-26.5,20.35,0.7);
		tv.rotation.set(-Math.PI*0.5,0,Math.PI*0.5);
		scene.add(tv);
	});

	loader.load('models/the_cake_is_a_lie/scene.gltf', function(gltf){
		cake = gltf.scene; //figlio della scena
		cake.castShadow = true;
		// portalGun.scale.set(0.01,0.01,0.01)
		cake.position.set(-0.55,15,4.93);
		//cake.rotation.set(-Math.PI*0.5,0,Math.PI*0.5);
		//scene.add(cake);
	});




	loader.load('portalradio.gltf', function(gltf){

		
		//console.log(dumpObject(gltf.scene).join('\n'));
		radio = gltf.scene; //figlio della scena
		radio = radio.getObjectByName( "Radio002", true );
		scene.add(radio);
		radio.position.set(11.87, 20, -3.5);
		radio.rotation.set(0,-Math.PI*0.5 - Math.PI/8,0);
		radio.add(RadioMusic);
		
		tv.castShadow = true;
		tv.position.set(-26.5,20.35,0.7);
		tv.rotation.set(-Math.PI*0.5,0,Math.PI*0.5);
		scene.add(tv);
	});

	var video = document.getElementById( 'video' );

	//video.preload = 'auto';
	//video.autoload = true;

	videoTexture = new THREE.VideoTexture( video );
	videoTexture.minFilter = THREE.LinearFilter;
	videoTexture.magFilter = THREE.LinearFilter;
	videoTexture.format = THREE.RGBFormat;

	boundingBoxTV = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), new THREE.MeshBasicMaterial({map	: videoTexture}), 0 );
	//boundingBoxfloor = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), new THREE.MeshPhongMaterial({color:0xff0000,  wireframe:false}),0 );
	boundingBoxTV.material.visible = true;
	boundingBoxTV.receiveShadow = true;
	boundingBoxTV.castShadow = true;
	boundingBoxTV.position.set(-26.2,20.35,0.7);
	boundingBoxTV.scale.set(0.4,5.69,9.8);
	scene.add(boundingBoxTV);
	boundingBoxTV.layers.enable(1);


	loader.load('models/portalGun/scene.gltf', function(gltf){
		portalGun = gltf.scene.children[0]; //figlio della scena
		portalGun.castShadow = true;
		character.camera.add(portalGun);
		portalGun.scale.set(0.0090,0.0090,0.0090)
		portalGun.position.set(0.15,-0.08,-0.2);
		portalGun.rotation.set(-Math.PI*0.5,0,Math.PI*0.5*0.1);
	});

	var materialCube = Physijs.createMaterial(
		new THREE.MeshPhongMaterial({color:0xfff00,  wireframe:true}),
		1
	);

	boundingBoxCube = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), materialCube,1 );
	// The cube can have shadows cast onto it, and it can cast shadows
	boundingBoxCube.friction = 10;
	boundingBoxCube.receiveShadow = true;
	boundingBoxCube.castShadow = true;
	boundingBoxCube.material.visible = false;

	
	loader.load('models/wheatley/scene.gltf', function(gltf){
		wheatley = gltf.scene.children[0]; //figlio della scena
		wheatley.traverse( function ( child ) {
			
			if ( child instanceof THREE.Mesh ) {
				
				child.castShadow = true;
				child.receiveShadow = true;
				
				
			}
		});

		wheatley.castShadow = true;
		wheatley.scale.set(0.05,0.05,0.05)
		wheatley.position.set(4.3, 17.84, 14);
		wheatley.rotation.set(-Math.PI,-Math.PI*0.5,0);

		scene.add(wheatley);
		wheatley.layers.enable(1);

	});
	


	loader.load('models/portal_cube/scene.gltf', function(gltf){
		portal_cube = gltf.scene; //figlio della scena
		portal_cube.traverse( function ( child ) {
			
			if ( child instanceof THREE.Mesh ) {
				
				child.castShadow = true;
				child.receiveShadow = true;
			
				
			}
		});

	
		boundingBoxCube.add(portal_cube)
		portal_cube.scale.set(0.50,0.50,0.50)
		boundingBoxCube.name = "boundingBoxCube";
		boundingBoxCube.position.set(7.45,22,-7);
		boundingBoxCube.scale.set(1.80,1.80,1.80)
		scene.add(boundingBoxCube);
		boundingBoxCube.layers.enable(1);


		boundingBoxCube2 = boundingBoxCube.clone(true);
		boundingBoxCube2.name = "boundingBoxCube";
		boundingBoxCube2.position.set(20.1,18.4,19.4);
		boundingBoxCube2.material.visible = false;
		boundingBoxCube2.layers.enable(1);
		

		boundingBoxCube3 = boundingBoxCube.clone(true);
		boundingBoxCube3.name = "boundingBoxCube";
		boundingBoxCube3.position.set(20,25,5.35);
		//boundingBoxCube3.position.set(19.6,38.6,19.3);
		boundingBoxCube3.material.visible = false;

		//boundingBoxCube2.scale.set(2,2,2)
		//scene.add(boundingBoxCube3);
		boundingBoxCube3.layers.enable(1);
		
	});

	var material2 = Physijs.createMaterial(new THREE.MeshPhongMaterial({color:0xfffff,  wireframe:false}),1);

	boundingBoxTurrets = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), material2, 0 );
	boundingBoxTurrets.position.set(-17.5 , 22, -14.89);
	boundingBoxTurrets.scale.set(8.29,5.39,4.5);
	boundingBoxTurrets.material.visible = false;
	boundingBoxCube3.layers.enable(1);

	scene.add(boundingBoxTurrets);

	var material3 = Physijs.createMaterial(new THREE.MeshPhongMaterial({color:0xffffff,  wireframe:false}),1);


	boundingBoxAusiliar = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), material3,0 );
	// The cube can have shadows cast onto it, and it can cast shadows
	boundingBoxAusiliar.receiveShadow = true;
	boundingBoxAusiliar.castShadow = true;
	boundingBoxAusiliar.position.set(17.68, 37, 19.68);
	boundingBoxAusiliar.rotation.set(0,0,Math.PI/2);
	boundingBoxAusiliar.scale.set(5.6,0.3, 4.2)
	scene.add(boundingBoxAusiliar);
	boundingBoxAusiliar.layers.enable(1);


	boundingBoxAusiliar1 = new Physijs.BoxMesh( new THREE.BoxGeometry(1,1,1), material3,0 );
	// The cube can have shadows cast onto it, and it can cast shadows
	boundingBoxAusiliar1.receiveShadow = true;
	boundingBoxAusiliar1.castShadow = true;
	boundingBoxAusiliar1.position.set(19.95, 37.4, 17.48);
	boundingBoxAusiliar1.rotation.set(0,Math.PI/2,Math.PI/2);
	boundingBoxAusiliar1.scale.set(4.69,0.4, 4.89)
	scene.add(boundingBoxAusiliar1);
	boundingBoxAusiliar1.layers.enable(1);

	
	
	//BODY OF MY ROBOTS
	//#region 
	//ASSE Z E' VERSO L'ALTO, QUELLO Y è ORIZZONTALE
	Body = new THREE.Mesh( new THREE.BoxGeometry(), new THREE.MeshPhongMaterial({visible:false}));
    scene.add(Body);
    bodyCapsule = new THREE.Mesh( new THREE.SphereGeometry(1,18,18,0,Math.PI*2*0.95) , new THREE.MeshPhongMaterial({color:0x8C8D91, emissiveIntensity:0.7, shininess: 70}));
    bodyCapsule.material.side = THREE.DoubleSide;
    bodyCapsule.castShadow=true;
    Body.add(bodyCapsule);
    bodyCapsule.scale.set(0.9,0.8,0.8)
    bodyCapsule.rotation.set(Math.PI/2,0,Math.PI/2);
    bodyCapsule.position.set(0,0.2,1);
	CreateBody(Body, character.camera);

	floatingEye = new THREE.Mesh( new THREE.SphereGeometry(1,12,12,0) , new THREE.MeshPhongMaterial({color:0x363BEC, emissiveIntensity:0.7, shininess:70}));
	floatingEye.position.set(0,0,0);
	floatingEye.scale.set(0.4,0.4,0.4);
	bodyCapsule.add(floatingEye);
	
	spotLight.castShadow = true;
	spotLight.shadow.camera.near = 0;
	spotLight.shadow.camera.far = 5;
	spotLight.shadow.camera.fov = 10;
	spotLight.angle = Math.PI/12;
	character.camera.add( spotLight );
	targetSpot = new THREE.Object3D();
	character.camera.add(targetSpot);
	targetSpot.position.set(0,0.65,-5);
	spotLight.target = targetSpot;
	// var spotLightHelper = new THREE.SpotLightHelper( spotLight );
	// scene.add( spotLightHelper );
	
	
	//ASSE X DELLA SFERA USCENTE DA "DAVANTI" IL CORPO, ASSE Z è ORIZZONTALE AL CORPO
	upperSphereR = new THREE.Mesh( new THREE.SphereGeometry(0.3), new THREE.MeshPhongMaterial({color:0x00000, emissiveIntensity:0.7, shininess : 70}));	
	upperSphereR.position.set(0,-1.2,0.3);
	upperSphereR.rotation.set(-Math.PI*0.5,0,-Math.PI/8)
	bodyCapsule.add(upperSphereR);
	
	upperLegR = new THREE.Mesh( new THREE.BoxGeometry(0.2,1.3,0.2), new THREE.MeshPhongMaterial({color:0x8C8D91, emissiveIntensity:0.7, shininess : 70}));	
	upperLegR.position.set(0,-0.5,0);
	upperSphereR.add(upperLegR);
	
	LowerSphereR = new THREE.Mesh( new THREE.SphereGeometry(0.2), new THREE.MeshPhongMaterial({color:0x00000, emissiveIntensity:0.7, shininess : 70}));	
	LowerSphereR.position.set(0,-0.7,0);
	upperLegR.add(LowerSphereR);
	
	LowerLegR = new THREE.Mesh( new THREE.BoxGeometry(0.2,1.3,0.2), new THREE.MeshPhongMaterial({color:0x8C8D91, emissiveIntensity:0.7, shininess : 70}));	
	LowerLegR.position.set(0,-0.5,0);
	LowerSphereR.add(LowerLegR);
	
	feetR = new THREE.Mesh( new THREE.BoxGeometry(0.85,0.2,0.6), new THREE.MeshPhongMaterial({color:0x00000, emissiveIntensity:0.7, shininess: 70}));	
	feetR.position.set(0,-0.7,0);
	feetR.rotation.set(0,0,Math.PI/128)
	LowerLegR.add(feetR);
	
	//ASSE X DELLA SFERA USCENTE DA "DAVANTI" IL CORPO, ASSE Z è ORIZZONTALE AL CORPO
	upperSphereL = new THREE.Mesh( new THREE.SphereGeometry(0.3), new THREE.MeshPhongMaterial({color:0x00000, emissiveIntensity:0.7, shininess : 70}));	
	upperSphereL.position.set(0, 1.2,0.3);
	upperSphereL.rotation.set(-Math.PI*0.5,0,-Math.PI/8)
	bodyCapsule.add(upperSphereL);
	
	upperLegL = new THREE.Mesh(  new THREE.BoxGeometry(0.2,1.3,0.2), new THREE.MeshPhongMaterial({color:0x8C8D91, emissiveIntensity:0.7, shininess : 70}));	
	upperLegL.position.set(0,-0.5,0);
	upperSphereL.add(upperLegL);
	
	
	LowerSphereL =new THREE.Mesh( new THREE.SphereGeometry(0.2), new THREE.MeshPhongMaterial({color:0x00000, emissiveIntensity:0.7, shininess :70}));	
	LowerSphereL.position.set(0,-0.7,0);
	upperLegL.add(LowerSphereL);
	
	LowerLegL = new THREE.Mesh( new THREE.BoxGeometry(0.2,1.3,0.2), new THREE.MeshPhongMaterial({color:0x8C8D91, emissiveIntensity:0.7, shininess :70}));	
	LowerLegL.position.set(0,-0.5,0);
	LowerSphereL.add(LowerLegL);
	
	feetL = new THREE.Mesh(  new THREE.BoxGeometry(0.85,0.2,0.6), new THREE.MeshPhongMaterial({color:0x000000,  emissiveIntensity:0.7, shininess : 70}));	
	feetL.position.set(0,-0.7,0);
	feetL.rotation.set(0,0,Math.PI/128)
	LowerLegL.add(feetL);
	
	//#endregion
	

	///////////////////
//#region
var level1_data0=[0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				1,1,1,1,1,1,1,1,1,1,1,1,
				1,1,1,1,1,1,1,1,1,1,1,1,
				1,1,1,1,1,1,1,1,1,1,1,1,
				1,1,1,1,1,1,1,1,1,1,1,1,
				1,1,1,1,1,1,1,1,1,1,1,1,
				1,1,1,1,1,1,1,1,1,1,1,1,
				0,0,0,0,0,0,0,1,1,1,1,1]

var level1_data=[0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,1,1,1,
				1,1,1,1,1,1,1,1,1,0,0,1,
				1,1,1,1,1,0,0,1,1,0,0,1,
				1,1,1,1,1,0,0,0,0,0,0,1,
				1,1,1,1,1,0,1,0,0,0,0,1,
				1,1,1,1,1,0,0,0,0,0,0,1,
				1,1,1,1,1,1,1,1,0,0,0,1,
				0,0,0,0,0,0,0,1,0,0,1,1]

var level1_data1=[0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,1,1,1,1,
				1,1,1,1,1,1,1,1,1,0,0,1,
				1,1,1,1,1,0,0,1,1,0,0,1,
				1,1,1,1,1,0,0,0,0,0,0,1,
				1,1,1,1,1,1,1,0,0,0,0,1,
				1,1,1,1,1,0,0,0,0,0,0,1,
				1,1,1,1,1,1,1,1,0,0,0,1,
				0,0,0,0,0,0,0,1,0,0,1,1]

var level1_data2=[1,1,1,1,1,1,1,1,1,1,1,1,
				1,1,1,1,1,1,1,1,1,1,1,1,
				0,0,0,0,1,1,1,1,1,0,0,1,
				0,0,0,0,0,0,0,1,1,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1]

var level1_data3=[1,0,0,0,0,0,0,1,1,1,1,1,
				1,0,0,0,0,0,0,1,1,1,1,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,1,1]

var level1_data4=[1,0,0,0,0,0,0,1,1,1,1,1,
				1,0,0,0,0,0,0,1,1,1,1,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,1,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,0,1,
				0,0,0,0,0,0,0,0,0,0,1,1]

	
var level_data_final = [level1_data0, level1_data, level1_data1, level1_data2, level1_data3, level1_data3, level1_data4];

LoadLevel(level_data_final, 12, 9, 12*5, 9*5, 7*5, new THREE.Vector3(0, 2.5, 2.5));

//#endregion
	
	
	// key frame = [ UpperSphereR, UpperSphereL, LowerSphereR, LowerSphereL]
	
	var start_keys = [0, 0, 0, 0];
	var end_keys =   [0, 0, 0, 0];

	standStill_anim = CreateAnimation(start_keys, end_keys, 1, true, ping_pong = false);

	 var start_keys = [-Math.PI/8 + Math.PI/6, -Math.PI/8 -Math.PI/6,Math.PI/10,Math.PI/10];
     var end_keys =   [-Math.PI/8 -Math.PI/6,- Math.PI/8+Math.PI/6,0, 0];

	 walk_animForward = CreateAnimation(start_keys, end_keys, 1.5, true, ping_pong = true, 0.5);
	 
	 var start_keys = [-Math.PI/8, -Math.PI/8 , 0, 0];
     var end_keys =   [ -Math.PI/8 -Math.PI/2,-Math.PI/8-Math.PI/2, Math.PI/2, Math.PI/2];

	jump_anim = CreateAnimation(start_keys, end_keys, 1.5, true, ping_pong = true,0.5);

	var start_keys = [16.84];
	var end_keys =   [ 18.84];

	  wheatney_fluctuation = CreateAnimation(start_keys, end_keys, 3.0, true, ping_pong = true, smoothLerp = true);
	  
	//anim_state = InitAnimState(walk_anim) //nell'init se voglio inizi subito 

	//anim_stateWalkForward = InitAnimState(walk_animForward)
	wheatleyAnim_state = InitAnimState(wheatney_fluctuation)
	anim_state = InitAnimState(standStill_anim)


	
	//animate();
	
}

var s = new THREE.Vector3();



/*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ */

var justSpawned = true;
var anim_state;
function animate()
{
	
	var delta = clock.getDelta();
	//Println(1/delta);

	//PrintVector(character.camera.position);
	animationHandler();
	angle = AnimationPlayer(anim_state, delta);
	positWheat = AnimationPlayer(wheatleyAnim_state, delta);

	wheatley.position.y = positWheat[0];
	
	upperSphereR.rotation.set(-Math.PI*0.5,0,angle[0]);
	upperSphereL.rotation.set(-Math.PI*0.5,0,angle[1]);
	
	LowerSphereR.rotation.set(0,0,angle[2]);
	LowerSphereL.rotation.set(0,0,angle[3]);
	
	boundingBoxTV.material.map.needsUpdate = true;

	PrintVector(character.camera.position);


	if(justSpawned && character.camera.position.y <= 17.5) {
		document.getElementById("target").style.display = "block";
		$("#target").fadeOut(8000);
		justSpawned=false;
	}
	Respawn();

//	MoveObject(radio);


	UpdateBody(delta);
	if(turnOnOffLight) spotLight.power = 0;
	else if(!turnOnOffLight) spotLight.power = Math.PI;

	
	if(grabbed) {UpdateGrab();}


	wheatley.lookAt(character.camera.position);
	var eul = new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI*0.5,0,Math.PI)); 
	wheatley.quaternion.multiply(eul);
	
	
	
	activateButton(boundingBoxButton);
	activateButton2(boundingBoxButton2);
	activateButton3(boundingBoxButton3);
	HandleButtons();

	//ordine importante!
	scene.simulate();

    PortalsUpdate(character.camera,scene, delta, GetBodyWidth());
    bodyCapsule.traverse(SetVisibilityFalse);


    UpdateCharacter(scene,delta);
	bodyCapsule.traverse(SetVisibilityTrue);
	////////////////////
	
	//setTimeout( function() {

		    requestAnimationFrame( animate );
	
	//	}, 1000 / 60 );



	

}

function animationHandler()
{
	var anim;
	if(IsJumping()) anim = jump_anim;
	else if(IsFalling()) anim = standStill_anim;
	else if(GetLocalVelocity().lengthSq() > 0.01) anim = walk_animForward;
	else anim = standStill_anim;

	if(anim!=anim_state["animation"])
	anim_state = InitAnimState(anim);
}



function SetVisibilityTrue(child) 
{
    if(child instanceof THREE.Mesh)
        child.material.visible = true;
}

function SetVisibilityFalse(child) 
{
    if(child instanceof THREE.Mesh)
        child.material.visible = false;
}
var cam_load;
function CameraLoader()
{
	cam_load = new THREE.PerspectiveCamera();
	cam_load.position.set(testRoom.position.x, testRoom.position.y + 20, testRoom.position.z);

	UpdateCameraLoader();
}

function UpdateCameraLoader()
{
	cam_load.rotation.y += DegreeToRad(10);
	if(cam_load.rotation.y >= DegreeToRad(1000))
		EndLoad();
	else 
	{
		renderer.render(scene, cam_load);
		requestAnimationFrame(UpdateCameraLoader);
	}
}

function EndLoad()
{
	$("#schermata_caricamento").fadeOut(850);
	animate();
}


var cubespawned1 = false;
var cubespawned2 = false;

function HandleButtons()
{	//Println(pressed);

	if(pressed && !cubespawned1)
	{
		
		scene.add(boundingBoxCube2);
		cubespawned1 = true;
	}

	if(pressed2 && !cubespawned2)
	{	
		scene.add(boundingBoxCube3);
		cubespawned2 = true;
	}

	if(pressed && pressed2 && pressed3)
	{
		RadioMusic.pause();
		ending.play();
		boundingBoxTV.material.map = textureEnding;
		ambientLight.intensity = 0.2;
		dirLight.intensity = 0.0;
		scene.add(spotLight1);
		scene.add(cake);
	}

}

var doorOpened = false;
var startDoorAngle = 0;
var endDoorAngle = Math.PI*0.5;

function OpenDoor(door,buttonPressed,period,delta)
{

	if(buttonPressed && !doorOpened)
	{
		//Println("buttonPressed && !doorOpened");
		var doorAngle = new THREE.Vector3(door.rotation.x,door.rotation.y, door.rotation.z);
		var endAngle =new THREE.Vector3(door.rotation.x, endDoorAngle, door.rotation.z);


		timerdoor += delta*10;
		alphadoor = timerdoor/(period/4);

		alphadoor = Clamp(alphadoor,0,1);

		doorAngle.lerp(endAngle,alphadoor);
		door.rotation.set(door.rotation.x, doorAngle.y, door.rotation.z)


		if(alphadoor >= 1)
		{
			timerdoor = 0;
			//currentRot = doorAngle.z;
			doorOpened=true;
		}
	}

	else if(buttonPressed && doorOpened) {/*Println("buttonPressed && doorOpened");*/ doorOpened = true;}

	else if(!buttonPressed && doorOpened)
	{
		//Println("!buttonPressed && doorOpened");

		var doorAngle = new THREE.Vector3(door.rotation.x, door.rotation.y, door.rotation.z);
		var endAngle =new THREE.Vector3(door.rotation.x, startDoorAngle, door.rotation.z);
		timerdoor += delta*10;
		alphadoor = timerdoor/(period/4);
		alphadoor = Clamp(alphadoor,0,1);

		doorAngle.lerp(endAngle,alphadoor);
		//Println(doorAngle.y);
		door.rotation.set(doorAngle.x, doorAngle.y, door.rotation.z);

		if(alphadoor>= 1)
		{
			timerdoor = 0;
			doorOpened=false;
		}
	}

	else if(!buttonPressed && !doorOpened) {/*Println("!buttonPressed && !doorOpened");*/ doorOpened= false;}

}

function activateButton(boundingBoxButton)
{
	raycasterB = new THREE.Raycaster(new THREE.Vector3(boundingBoxButton.position.x,boundingBoxButton.position.y,boundingBoxButton.position.z), new THREE.Vector3(0,1,0));
	
	//calculate objects intersecting the picking ray
	 var intersects = raycasterB.intersectObjects( scene.children, true );
	 if(intersects[0] == undefined) {pressed = false; return;}
	 //Println(intersects[0].object.position.x);
	var posx = intersects[0].object.position.x;
	var posy = intersects[0].object.position.y;
	var posz = intersects[0].object.position.z;

	if(intersects.length>0)
	{
		var distance = new THREE.Vector3( posx-boundingBoxButton.position.x, posy-boundingBoxButton.position.y, posz-boundingBoxButton.position.z);
		//Println(distance.y);
		//if(intersects[0].object.name != undefined) Println(intersects[0].object.name)
		if(distance.length() <= 1.08 && intersects[0].object.name == "boundingBoxCube") {
		//	Println("cube pressing the button!");
			pressed = true;
			
		}
		else pressed = false;
	}
//	if(!pressed) Println("cube NOT pressing the button!");
	

}
function activateButton2(boundingBoxButton)
{
	raycasterB = new THREE.Raycaster(new THREE.Vector3(boundingBoxButton.position.x,boundingBoxButton.position.y,boundingBoxButton.position.z), new THREE.Vector3(0,1,0));

	//var buttonCenter = new THREE.Vector2(0,0);
	
	//calculate objects intersecting the picking ray
	 var intersects = raycasterB.intersectObjects( scene.children, true );
	 if(intersects[0] == undefined) {pressed2 = false; return;}
	 //Println(intersects[0].object.position.x);
	var posx = intersects[0].object.position.x;
	var posy = intersects[0].object.position.y;
	var posz = intersects[0].object.position.z;

	if(intersects.length>0)
	{
		var distance = new THREE.Vector3( posx-boundingBoxButton.position.x, posy-boundingBoxButton.position.y, posz-boundingBoxButton.position.z);
		//Println(distance.y);
		//if(intersects[0].object.name != undefined) Println(intersects[0].object.name)
		if(distance.length() <= 1.08 && intersects[0].object.name == "boundingBoxCube") {
		//	Println("cube pressing the button!");
			pressed2 = true;
			
		}
		else pressed2 = false;
	}
	//if(!pressed) Println("cube NOT pressing the button!");
	

}

function activateButton3(boundingBoxButton)
{
	raycasterB = new THREE.Raycaster(new THREE.Vector3(boundingBoxButton.position.x,boundingBoxButton.position.y,boundingBoxButton.position.z), new THREE.Vector3(0,1,0));
	raycasterA = new THREE.Raycaster(new THREE.Vector3(boundingBoxButton.position.x-0.1,boundingBoxButton.position.y,boundingBoxButton.position.z), new THREE.Vector3(0,1,0));

	//var buttonCenter = new THREE.Vector2(0,0);
	
	//calculate objects intersecting the picking ray
	 var intersects = raycasterB.intersectObjects( scene.children, true );
//	 var intersects1 = raycasterA.intersectObjects( scene.children, true );

	 if(intersects[0] == undefined /*|| intersects1[0]==undefined*/) {pressed3 = false; return;}
	 //Println(intersects[0].object.position.x);
	// if(intersects)
	var posx = intersects[0].object.position.x;
	var posy = intersects[0].object.position.y;
	var posz = intersects[0].object.position.z;

	if(intersects.length>0)
	{
		var distance = new THREE.Vector3( posx-boundingBoxButton.position.x, posy-boundingBoxButton.position.y, posz-boundingBoxButton.position.z);
	//	Println(distance.y);
		//if(intersects[0].object.name != undefined) Println(intersects[0].object.name)
		if(distance.length() <= 1.08 && intersects[0].object.name == "boundingBoxCube") {
			//Println("cube pressing the button!");
			pressed3 = true;
			
		}
		else pressed3 = false;
	}
	//if(!pressed) Println("cube NOT pressing the button!");
	

}

//window.onload = init;

