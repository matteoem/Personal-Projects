var character;
var gravity = -9.8;
var fpc_raycaster = new THREE.Raycaster();
var ignore_tags = [];

function CreateCharacter(dom_element, scene, fov, aspect, near, far)
{
	var camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    character = { camera:camera, delta:0, look_speed:0.1, forward:0, back:0, right:0, left:0, running:false, falling:false, movement_speed:5, run_speed:10, jump_force:10, height:2, width:0.5, body_margin:0.3, step_height:0.1, gravity_acc:0, jump_acc:0, last_pos:new THREE.Vector3(), body:null, force:new THREE.Vector3() };

	dom_element.addEventListener( 'mousemove', FPC_onMouseMove, false );
	dom_element.addEventListener('keydown', FPC_onKeyDown, false);
    dom_element.addEventListener('keyup', FPC_onKeyUp);
    
    scene.add(character.camera);
    raycaster.layers.set(1);
}

function AddPhysicBody(scene)
{
    if(character.body != null) return;

    var w = character.width + character.body_margin;
    var mesh = new Physijs.BoxMesh(new THREE.BoxGeometry(w, w, w), new THREE.MeshPhongMaterial({color:0x0000ff, wireframe:true}), 1);
    var body = { mesh:mesh };
    character.body = body;
    
    scene.add(mesh);
    SetMeshVisibility(false);
    mesh.layers.enable(2);
}

function AddIgnoreTag(tag_name)
{
    if(!ignore_tags.includes(tag_name))
        ignore_tags.push(tag_name);
}

function SetMeshVisibility(state)
{
    if(character.body == null) return;
    character.body.mesh.material.visible = state;
}

function FPC_onMouseMove(event)
{
    var delta = character.delta;// clock.getDelta();

    var movementX = event.movementX || event.mozMovementX || event.webkitMovementX || 0;
    var movementY = event.movementY || event.mozMovementY || event.webkitMovementY || 0;

    var euler = new THREE.Euler( 0, 0, 0, 'YXZ' );

    euler.setFromQuaternion( character.camera.quaternion );

    euler.y -= movementX * character.look_speed * delta;
    euler.x -= movementY * character.look_speed * delta;
    euler.x = Math.max( -Math.PI*0.5, Math.min( Math.PI*0.5, euler.x ) );

    character.camera.quaternion.setFromEuler( euler );
}

function FPC_onKeyDown(event) 
{
    switch ( event.which ) 
    {
		//case 38: /*up*/
		case 87: /*W*/ character.forward = -1; break;

		//case 37: /*left*/
		case 65: /*A*/ character.left = -1; break;

		//case 40: /*down*/
		case 83: /*S*/ character.back = 1; break;

		//case 39: /*right*/
		case 68: /*D*/ character.right = 1; break;

		case 16: /*shift*/ character.running = true; break;

		case 32: Jump(); break;
	}
}

function FPC_onKeyUp ( event )
{
    switch ( event.which ) 
    {
		//case 38: /*up*/
		case 87: /*W*/ character.forward = 0; break;

		//case 37: /*left*/
		case 65: /*A*/ character.left = 0; break;

		//case 40: /*down*/
		case 83: /*S*/ character.back = 0; break;

		//case 39: /*right*/
        case 68: /*D*/ character.right = 0; break;
        
		case 16: /*shift*/ character.running = false; break;
	}
}

function Jump()
{
    if(!character.falling)
        character.jump_acc = character.jump_force;
        //character.force.y = character.jump_force;
}

function UpdateForce(delta, direction)
{
    if(character.jump_acc > 0)
        character.jump_acc = Math.max(0, character.jump_acc + gravity * delta); 
    
    if(character.falling)
    {
            character.gravity_acc += gravity * delta;
            character.gravity_acc = Math.max(character.gravity_acc, gravity*3);
    }
    else character.gravity_acc = 0;
        
    direction.y += (character.gravity_acc + character.jump_acc) * delta;
    character.force.lerp(direction, 10 * delta); 
}

function Move(delta)
{
    var dt = delta;// Math.max(delta, 0.016);
    
    var x = (character.forward + character.back);
    var y = (character.left + character.right);
    var dir = new THREE.Vector3(y, 0, x).applyQuaternion(character.camera.quaternion);
    dir.y = 0;

    var speed = (character.running ? character.run_speed : character.movement_speed) * dt;
    dir.normalize().multiplyScalar(speed);

    UpdateForce(dt, dir)

    //dir.add(character.force);

    var new_pos = character.camera.position.clone()
    new_pos.add(character.force);
    new_pos.y = TraceDown(scene, new_pos);

    if(!MovementTrace(new_pos))
    {
        character.last_pos = new_pos.clone();    
        character.camera.position.copy(new_pos);
    }
    else
    {
        character.camera.position.copy(character.last_pos);
        character.camera.position.y = new_pos.y;
    } 
}

function TraceDown(scene, origin)
{
    var w = character.width / 2;

    var o1 = new THREE.Vector3(w, 0, 0);
    var o2 = new THREE.Vector3(-w, 0, 0);
    var o3 = new THREE.Vector3(0, 0, w);
    var o4 = new THREE.Vector3(0, 0, -w);
    var origins = [o1, o2, o3, o4];

    for(var i = 0; i < 4; i++)
    {
        raycaster.set(origin.clone().add(origins[i]), new THREE.Vector3(0,-1,0));
        var objs = raycaster.intersectObjects(scene.children, true);
        
        if(objs.length == 0 || objs[0].distance > character.height + 0.1 || ignore_tags.includes(objs[0].object.name))
            continue;
        
        character.falling = false;
        return objs[0].point.y + character.height;
    }

    character.falling = true;
    return origin.y;
}

function MovementTrace(origin)
{
    var w = character.width / 2;

    var origin_half_height = origin.clone();

    var c1 = new THREE.Vector3(-w, 0, 0);
    var c2 = new THREE.Vector3(w, 0, 0);
    var c3 = new THREE.Vector3(0, 0, w);
    var c4 = new THREE.Vector3(0, 0, -w);
    var c5 = new THREE.Vector3(0, w, 0);
    var c6 = new THREE.Vector3(0, -w, 0);

    var origins = [c1, c2, c3, c4, c5, c6];

    for(var i = 0; i < 6; i++)
    {
        var start = origin_half_height;
        var end_dir = origin_half_height.clone().add(origins[i]).sub(origin_half_height).normalize();

        raycaster.set(start, end_dir);
        var objs = raycaster.intersectObjects(scene.children, true);
        
        dist = w;
        if(objs.length > 0 && objs[0].distance <= dist) return true;
    }

    return false;
}

function MoveBody()
{
    if(character.body == null) return;

    var pos = character.camera.position.clone();
    character.body.mesh.position.copy(pos);
    character.body.mesh.__dirtyPosition = true;
    character.body.mesh.rotation.set(0,0,0);
    character.body.mesh.__dirtyRotation = true;
}

function UpdateCamera(delta, speed)
{
    var euler = new THREE.Euler( 0, 0, 0, 'YXZ' );

    euler.setFromQuaternion( character.camera.quaternion );
    euler.z = Lerp(euler.z, 0, delta * speed);

    character.camera.quaternion.setFromEuler( euler );
}

function UpdateCharacter(scene, delta)
{
    character.delta = delta;

    Move(delta);
    MoveBody();
    UpdateCamera(delta, 5);

	renderer.render(scene, character.camera);
}

function GetBodyWidth()
{
    return character.width + character.body_margin;
}

function DrawDebugLine(scene, origin)
{
    var w = character.width / 2;
    
    var h = character.height / 2;
    var h2 = character.height / 2 - character.step_height;
    
    var diag = character.diagonal;
    var diag2 = character.diagonal_step;

    var origin_half_height = origin.clone().add(new THREE.Vector3(0, -h, 0));

    var u1 = new THREE.Vector3(-w, h, w);
    var u2 = new THREE.Vector3(w, h, w);
    var u3 = new THREE.Vector3(-w, h, -w);
    var u4 = new THREE.Vector3(w, h, -w);
    var d1 = new THREE.Vector3(-w, -h2, w);
    var d2 = new THREE.Vector3(w, -h2, w);
    var d3 = new THREE.Vector3(-w, -h2, -w);
    var d4 = new THREE.Vector3(w, -h2, -w);
    var c1 = new THREE.Vector3(-w, 0, 0);
    var c2 = new THREE.Vector3(w, 0, 0);
    var c3 = new THREE.Vector3(0, 0, w);
    var c4 = new THREE.Vector3(0, 0, -w);
    var c5 = new THREE.Vector3(0, h, 0);
    var c6 = new THREE.Vector3(0, -h2, 0);

    var origins = [u1, u2, u3, u4, d1, d2, d3, d4, c1, c2, c3, c4, c5, c6];
    for(var i = 0; i < 14; i++)
    {
        var material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
        var points = [];
        
        points.push(origin_half_height);
        points.push(origins[i].clone().add(origin_half_height));

        var geometry = new THREE.BufferGeometry().setFromPoints( points );
        var line = new THREE.Line( geometry, material );
        line.layers.enable(2);
        scene.add( line );
    }
}

function IsJumping()
{
    return character.falling && character.jump_acc > 0;
}

function IsFalling()
{
    return character.falling;
}

function GetLocalVelocity()
{
    return character.force;
}