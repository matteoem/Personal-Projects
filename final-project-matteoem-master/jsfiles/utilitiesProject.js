function PortalCollision(object, position, rotation, m_start, m_end)
{
    if(object == character.body.mesh)
    {
        character.camera.position.copy(position);
        character.camera.quaternion.copy(rotation);

        var m = m_start.clone().inverse();
        var force = character.force.clone().applyQuaternion(m);
        force.applyQuaternion(m_end);

        character.force.copy(force.multiplyScalar(-1));
    }
    else if(object instanceof Physijs.Mesh)
    {
        object.position.copy(position);
        object.__dirtyPosition = true;

        object.quaternion.copy(rotation);
        object.__dirtyRotation = true;

        object.setLinearVelocity(new THREE.Vector3(0,0,0));

        // var m = m_start.clone().inverse();
        // var force = object.getLinearVelocity().clone();
        // force.applyQuaternion(m);
        // force.applyQuaternion(m_end);

        // object.setLinearVelocity(force.multiplyScalar(-1));
    }

    if(object == grabObj)
        grabbed = false;
}

function PortalCollisionData(object)
{
    if(object == character.body.mesh) return character.camera.matrixWorld;
    else return object.matrixWorld;
}

function Lock()
{
	var havePointerLock = 'pointerLockElement' in document ||
    'mozPointerLockElement' in document ||
	'webkitPointerLockElement' in document;
		//CAMBIA BROWSER

	if(!havePointerLock) return;

	var element = document.body;
	element.requestPointerLock = element.requestPointerLock ||
	element.mozRequestPointerLock ||
	element.webkitRequestPointerLock;
	// Ask the browser to lock the pointer
	element.requestPointerLock();

	updateCharacter = true;
}



function UpdateGrab()
{
	if(!grabbed) return;
	var camerapos = new THREE.Vector3();
	var cameraforward = new THREE.Vector3();
	var objpos = new THREE.Vector3();

	character.camera.getWorldPosition(camerapos);
	character.camera.getWorldDirection(cameraforward);
	cameraforward.multiplyScalar(3.5);//distance of the grabbed object
	camerapos.add(cameraforward);

	grabObj.getWorldPosition(objpos);
	camerapos.sub(objpos); //direction 
	camerapos.multiplyScalar(10);
	grabObj.setLinearVelocity(camerapos);
	


	
}




function onKeyDown(event) {


	switch ( event.which ) {

		case 38: MoveforBack = 1; break;

	

		case 37: /*leftArrow*/ moveLR = -1; break;

		

		case 40: MoveforBack = -1; break;

		

		case 39: /*rightArrow*/ moveLR = 1; break;

		case 82: /*R*/ turnOnOffLight = !turnOnOffLight; break;

		case 85: /*U*/ UpDown = 1; break;
		case 80: /*P*/ UpDown = -1; break;

		case 187: /*+*/ scalePlus = 1; break;
		case 189: /*-*/ scaleMinus = -1; break;

		case 96: /*ins Zero*/ switchingScale++;
			if(switchingScale>3) switchingScale=0;
			break;

		
		case 17: //lock
			Lock();
			break;

		case 107: /*+ of the numPad*/
			findObject = true;

		case 69: 
		
		if(!grabbed){

			var cameraCenter = new THREE.Vector2(0,0);
			cameraCenter.y += 0.1;
			//Println(cameraCenter.y);
			raycasterE.setFromCamera( cameraCenter, character.camera );
			
			//calculate objects intersecting the picking ray
			var intersects = raycasterE.intersectObjects( scene.children, true );
			//Println(intersects[0].object.position.x);
			var posx = intersects[0].object.position.x;
			var posy = intersects[0].object.position.y;
			var posz = intersects[0].object.position.z;

			if(intersects.length>0)
				{
					var distance = new THREE.Vector3( posx-character.camera.position.x, posy-character.camera.position.y, posz-character.camera.position.z );
					if(distance.length() <= 4.0 && intersects[0].object.name == "boundingBoxCube") {


					
						// boundingBoxCube.position.set(0,0,-2.5);
						//Println(boundingBoxCube.position.z);
						grabObj = intersects[0].object;
						grabbed = true;
					}
				}
		}
		else if(grabbed)
		{
			grabbed = false;

		}	

	}
}



function MoveObject(object,raycasting = false)
{
	s = new THREE.Vector3(moveLR*speed, UpDown*speed, -MoveforBack*speed);
//	s1 = new THREE.Vector3(scalePlus*0.1,scalePlus*0.1,scalePlus*0.1);
	var speed = 0.1;
	switch ( switchingScale )
	{
		case 0:
			s1 = new THREE.Vector3(scalePlus*speed,scalePlus*speed,scalePlus*speed);
			s2 = new THREE.Vector3(scaleMinus*speed,scaleMinus*speed,scaleMinus*speed);
			break;
		case 1://solo lungo x
			s1 = new THREE.Vector3(scalePlus*speed,0,0);
			s2 = new THREE.Vector3(scaleMinus*speed,0,0);
			break;
		case 2:
			s1 = new THREE.Vector3(0,scalePlus*speed,0);
			s2 = new THREE.Vector3(0,scaleMinus*speed,0);
			break;
		case 3:
			s1 = new THREE.Vector3(0,0,scalePlus*speed);
			s2 = new THREE.Vector3(0,0,scaleMinus*speed);
			break;
			
		
	}



if(raycasting){


	if(findObject){
		var cameraCenter = new THREE.Vector2(0,0);
		raycasterE.setFromCamera( cameraCenter, character.camera );
		var intersects = raycasterE.intersectObjects( scene.children, true );

		if(intersects.length>0)
			{
				objName = intersects[0].object.name;

			}

			Println(objName);
	}

}

//	s2 = new THREE.Vector3(scaleMinus*0.1,scaleMinus*0.1,scaleMinus*0.1);
	else{
		object.__dirtyPosition = true;


		object.position.x += s.x;
		object.position.y += s.y;
		object.position.z += s.z;

		object.scale.x += s1.x + s2.x;
		object.scale.y += s1.y + s2.y;
		object.scale.z += s1.z + s2.z;

		object.__dirtyPosition = true;


		ClearConsole();
		Println("Position Vector:",true);
		Println("   ",true);
		PrintVector(object.position,true);
		Println(",       ",true);
		Println("scale Vector:",true);
		PrintVector(object.scale,true);
	}

}



function onKeyUp ( event ) {

	switch ( event.which ) {

		case 38: /*up*/ MoveforBack = 0; break;

		case 37: /*left*/ moveLR = 0; break;

		case 40: /*down*/ MoveforBack = 0; break;

		case 39: /*right*/ moveLR = 0; break;

		case 85: UpDown = 0; break;
		case 80:  UpDown = 0; break;

		case 187: /*+*/ scalePlus = 0; break;
		case 189: /*-*/ scaleMinus = -0; break;

		case 107: findObject = false; break;

	}

}

/* UTILITY FUNCTIONS FROM NOW ON */

var width = 0;
var height = 0;
function onResize( event ) {

	width = window.innerWidth;
	height = window.innerHeight * 0.9;
  
 	windowHalf.set( width / 2, height / 2 );
	
	 character.camera.aspect = width / height;
	 character.camera.updateProjectionMatrix();
	renderer.setSize( width, height );
				
}




function Println(text, append = false)
{
    var t = document.getElementById("debug").innerHTML;
    document.getElementById("debug").innerHTML = append ? t + "\n" + text : text;
}

function PrintVector(vector, append = false)
{
	Println(vector.x, append);
	Println(vector.y, true);
	Println(vector.z, true);
}




function onDocumentMouseDown(event)
{
  raycastMeshes(event);
}




function raycastMeshes(event) {

	var cameraCenter = new THREE.Vector2(0,0);
	cameraCenter.y += 0.1;
	raycaster.setFromCamera( cameraCenter, character.camera );

	//calculate objects intersecting the picking ray
	var intersects = raycaster.intersectObjects( scene.children, true );

	switch (event.which){

		case 1:
			if(intersects.length >0) {
				var pos = intersects[0].point;
				if(intersects[0].face == null) return;
				if(intersects[0].object.name == "portal") return;
				var norm = intersects[0].face.normal.clone();
                norm.transformDirection( intersects[0].object.matrixWorld );
				if(PlacePortal(0,pos,norm))
                {
                    if(portalGunSound.isPlaying)
                    {
                        portalGunSound.stop();
                        portalGunSound.play();
                    }
                    portalGunSound.play();
                }
				
			}
			break;

		case 3:
			if(intersects.length >0) {
				var pos = intersects[0].point;
				if(intersects[0].face == null) return;
				if(intersects[0].object.name == "portal") return;
				var norm = intersects[0].face.normal.clone();
                norm.transformDirection( intersects[0].object.matrixWorld );
				if(PlacePortal(1,pos,norm))
                {
                    if(portalGunSound.isPlaying)
                    {
                        portalGunSound.stop();
                        portalGunSound.play();
                    }
                    portalGunSound.play();
                }
			}
			break;
	}


}



function dumpObject(obj, lines = [], isLast = true, prefix = '') {
  const localPrefix = isLast ? '└─' : '├─';
  lines.push(`${prefix}${prefix ? localPrefix : ''}${obj.name || '*no-name*'} [${obj.type}]`);
  const newPrefix = prefix + (isLast ? '  ' : '│ ');
  const lastNdx = obj.children.length - 1;
  obj.children.forEach((child, ndx) => {
    const isLast = ndx === lastNdx;
    dumpObject(child, lines, isLast, newPrefix);
  });
  return lines;
}




//Lerp function, non richiede spiegazioni
function Lerp(start, end, alpha)
{
    return start + alpha*(end-start);
}
// -------------------------------------------------------------------------------- //


//mandando il parametro a da 0 a 1, facendolo variare come il seno di un angolo che varia da [0,pi], 
//rendo la variazione non uniforme nelll'arco dei valori. Facendo così vedro' piu velocemente la parte
//iniziale dell'animazione,mentre meno veloce l'inizio e la fine. E' piacevole da vedere,"smootha" il tutto
function SmoothLerp(start, end, alpha)
{
    var a = (Math.sin(alpha * Math.PI) + 1) * 0.5;
    return start + a*(end-start);
}
// -------------------------------------------------------------------------------- //


function ClearConsole(){
    document.getElementById("debug").innerHTML = "";

}

function Clamp(value, min, max)
{
    return Math.min(Math.max(value, min), max);
}

function RadToDegree(value)
{
	return value * 180 / Math.PI;
}

function DegreeToRad(value)
{
	return value * Math.PI / 180;
}


function CreateAnimation(start_keys, end_keys, duration, loop, ping_pong = false, blend_duration = 0.5, smoothLerp = false)
{
    var obj = new Object();
    obj["start_keys"] = start_keys;
    obj["end_keys"] = end_keys;
    obj["duration"] = duration;
    obj["loop"] = loop;
    obj["blend_duration"] = blend_duration;
	obj["ping_pong"] = ping_pong;
	obj["smoothLerp"] = smoothLerp;


    return obj;
}

/*initAnimState prende in ingresso l'animazione da inizializzare,e la vecchia animazione
e inizializza i valori dell'oggetto: azzera il timer, specifica che l'animazione non è finita(sta iniziando)
imposta quale è l'ultima animazione appena finita(old animation) e se deve iniziare o no il blending fra 2 animazioni
*/
function InitAnimState(animation, old_animation = null)
{
    var obj = new Object();
    obj["timer"] = 0;
    obj["anim_finished"] = false;
    obj["animation"] = animation;
    obj["old_animation"] = old_animation;
    obj["blending"] = old_animation != null;

    return obj;
}

// -------------------------------------------------------------------------------- //

/*
L'animationPlayer prende l'animation state che contiene tutte le informazioni a riguardo, e la esegue
se blending è false, altrimenti se blending è true significa che l'animazione è finita e deve eseguire il blending
*/
function AnimationPlayer(anim_state, delta_time)
{
   if(anim_state["blending"])
       return UpdateBlending(anim_state, delta_time);
    else return UpdateAnimation(anim_state, delta_time);
}

// -------------------------------------------------------------------------------- //


/*updateAnimation prende in input l'oggetto anim_state e il delta_time,che sarebbe la durata di un singolo frame
UpdateAnimation essenzialmente è cio' che esegue effettivamente l'animazione. Prende i key frames, li setta come inizio-fine,
crea il parametro alpha, ed esegue la lerp per ogni start key frame di ogni parte del corpo. 
Essenzialmente esegue la lerp da start ad end di ogni parte del corpo. La maggior parte delle volte, start e key
saranno identici,volendo muovere solo alcune parti del corpo, e dunque appare inutile farlo, se non fosse che
questa funzione si presenta come scalabile,e dunque generica.
*/

function UpdateAnimation(anim_state, delta_time)
{
    var animation = anim_state["animation"];
    var start = animation["start_keys"];
    var end = animation["end_keys"];
	var smoothlerp = animation["smoothLerp"];

  
    anim_state["timer"] += delta_time;                           //timer aumenta del tempo passato per eseguire un frame, ogni frame. Tiene il tempo
    var frac = anim_state["timer"] / animation["duration"];
    var alpha = Clamp(frac, 0, 1);

    if(animation["ping_pong"])
        alpha = (Math.sin(alpha * 2 * Math.PI) + 1) * 0.5;

	var results = [];
    for(var i = 0; i < start.length; i++)
    {
	
		var result;
		if(smoothlerp)result = SmoothLerp(start[i], end[i], alpha);
		else result = Lerp(start[i], end[i], alpha);
        results.push(result);
    }
    
    if(frac >= 1.0)
    {
        if(animation["loop"])
            anim_state["timer"] = 0;
        
        else anim_state["anim_finished"] = true;
    }

    return results;
}

// -------------------------------------------------------------------------------- //

/*
UpdateBlending serve a dare una sequenzialità alle azioni. E' sempre un interpolazione "smoothata",
che prende come start frame la fine della vecchia animazione e come fine l'inizio della nuova animazione
Esattamente come per l'UpdateAnimation, il blending lo si fa per ogni parte del corpo.
*/

function UpdateBlending(anim_state, delta_time)
{
    var animation = anim_state["animation"];
    var old_animation = anim_state["old_animation"];

    var start = old_animation["end_keys"];
    var end = animation["start_keys"];

    anim_state["timer"] += delta_time;
    var alpha = anim_state["timer"] / animation["blend_duration"];
    alpha = Clamp(alpha, 0, 1);

    var results = [];
    for(var i = 0; i < start.length; i++)
    {
        var result = SmoothLerp(start[i], end[i], alpha);
        results.push(result);
    }

    if(alpha >= 1.0)
        anim_state["blending"] = false;

    return results;
}
// -------------------------------------------------------------------------------- //


// x_width e y_width è la dimensione dell'array che uso come mappa. Width,Depth e Height sono le dimensioni del livello
function LoadLevel(data, x_width, y_width, width, depth, height, position)
{
	var num_levels = data.length;

	var w = width / x_width;
	var d = depth / y_width;
	var h = height / num_levels;

	for(var l = 0; l < num_levels; l++)
	{
		var level = data[l];

		for(var j = 0; j < y_width; j++)
		{
			for(var i = 0; i < x_width; i++)
			{
				var index = j * x_width + i;
				
				var value = level[index];
				if(value == 0) continue;
				
				var x = i * w + position.x - width / 2;
				var y = j * d + position.z - depth / 2;
				var p = l * h + position.y;

				var asset = SpawnAsset(value, w, h, d);
				asset.receiveShadow = true;
				asset.position.set(x, p, y);				
				scene.add(asset);
			}
		}
	}
}

function SpawnAsset(id, w, h, d)
{ 
	var randomColor = "#000000".replace(/0/g,function(){return (~~(Math.random()*16)).toString(16);});
	var materialMap = Physijs.createMaterial(
		new THREE.MeshPhongMaterial({color:randomColor,wireframe:true, transparent: false, opacity: 0.5, visible: false}),
		1
	);
	var mesh = new Physijs.BoxMesh(new THREE.BoxGeometry(w,h,d), materialMap, 0);
	mesh.layers.enable(1);
	return mesh;
}

function Respawn()
{
	if(character.camera.position.y <= -17) character.camera.position.set(-23.2,25.35,0.7);
	if(boundingBoxCube.position.y <=-17)boundingBoxCube.position.set(7.45,22,-7);
	if(boundingBoxCube2.position.y <=-17)boundingBoxCube.position.set(20.1,18.4,19.4);
	if(boundingBoxCube3.position.y <=-17)boundingBoxCube.position.set(20,25,5.35);
}