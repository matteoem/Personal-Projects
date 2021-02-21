var portals = [];
var last_obj;
var c_timer = 0;
var max_time = 0.1;
var resize_time = 0.2;

var _onCollisionData, _onCollision;

function CreatePortals(num_portals, scene, camera_fov, camera_aspect, camera_near, camera_far, buffer_width, buffer_height, portal_geometry, scale)
{
    if(num_portals <= 0) return null;

    for(var i = 0; i < num_portals; i++)
    {
        //CREATE CAMERA AND BUFFER
        var cam = new THREE.PerspectiveCamera(camera_fov, camera_aspect, camera_near, camera_far);
        var buffer = new THREE.WebGLRenderTarget(buffer_width, buffer_height, { minFilter: THREE.LinearFilter, magFilter: THREE.NearestFilter, anisotropy:2});

        //CREATE MATERIAL
        var customUniforms = { Utexture: {value:buffer} };

        var material = new THREE.ShaderMaterial({
            uniforms:customUniforms,
            vertexShader: document.getElementById("vertex-shader").textContent,
            fragmentShader: document.getElementById("fragment-shader").textContent,
        });
    
        //CREATE MESH
        var mesh = new Physijs.BoxMesh(portal_geometry[i], material);
        mesh.scale.copy(scale);

        //CREATE PORTAL AND ADD TO ARRAY
        var portal = { mesh:mesh, camera:cam, buffer:buffer, id:i, active:false, placed:false, scale:scale, resizing:false, resize_timer:0, activation_callback:null };
        portals.push(portal);

        //ADD CAMERA AND MESH TO SCENE
        scene.add(mesh);
        scene.add(cam);

        //CreateCameraHelpher(cam, scene);

        //REGISTER TO COLLISION EVENT
        mesh.addEventListener( 'collision', OnCollision);
    }
}

function RegisterActivationCallback(callback, portal)
{
    portal.activation_callback = callback;
}

function CreateCameraHelpher(camera, scene)
{
    var h = new THREE.CameraHelper(camera);
    var m = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 0.1), new THREE.MeshPhongMaterial());
    var m2 = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.05, 0.2), new THREE.MeshPhongMaterial());

    camera.add(m);
    m.add(m2);
    scene.add(h);

    m2.position.z = -0.1;
    m.position.set(0,0,-20);
}

function PlacePortal(portal_index, position, point_normal)
{
    var portal = portals[portal_index];
    if(!CanBePlaced(position, point_normal, portal)) return false; 

    var norm = new THREE.Vector3().copy(point_normal).multiplyScalar(0.02);
    portal.placed = true;

    //POSITION
    var pos = new THREE.Vector3().addVectors(position, norm);

    portal.mesh.position.copy(pos);
    portal.mesh.__dirtyPosition = true;

    //ROTATION
    var mx = new THREE.Matrix4().lookAt(position.add(point_normal), pos, new THREE.Vector3(0,1,0));
    portal.mesh.quaternion.setFromRotationMatrix(mx);
    portal.mesh.__dirtyRotation = true;

    //ACTIVATION
    ActivatePortal(portal);
    
    //RESIZE EFFECT
    portal.resizing = true;
    portal.resize_timer = 0;

    return true;
}

function CanBePlaced(point, normal, portal)
{
    var p = point.clone().add(normal.clone().multiplyScalar(1));
    var mx = new THREE.Matrix4().lookAt(point, p, new THREE.Vector3(0,1,0));
    var q = new THREE.Quaternion().setFromRotationMatrix(mx);
    
    var o1 = new THREE.Vector3(1, 0, 0);
    var o2 = new THREE.Vector3(-1, 0, 0);
    var o3 = new THREE.Vector3(0, 1, 0);
    var o4 = new THREE.Vector3(0, -1, 0);
    var origins = [o1, o2, o3, o4];
    
    for(var i = 0; i < 4; i++)
    {
        raycaster.set(p, origins[i].clone().applyQuaternion(q));
        var objs = raycaster.intersectObjects(scene.children, true);
        
        // var material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
        // var points = [];
        
        // points.push(p);
        // points.push(p.clone().add(origins[i].clone().applyMatrix4(mx).multiplyScalar(portal.scale.y)));
        // Println(objs[0].distance);

        // var geometry = new THREE.BufferGeometry().setFromPoints( points );
        // var line = new THREE.Line( geometry, material );
        // line.layers.enable(2);
        // scene.add( line );

        if(objs.length > 0 && objs[0].distance <= portal.scale.y)
            return false
    }
    return true;
}

function ActivatePortal(portal)
{
    var other = portals[(portal.id + 1) % portals.length];
    if(other.placed)
    {
        portal.active = true;
        portal.mesh.name = "portal";
        portal.activation_callback();

        if(!other.active) ActivatePortal(other);
    }
}

function UpdatePortalsCameras(camera, scene, character_width)
{
    var num_portals = portals.length;
    if(num_portals <= 0) return;

    var world_camera_pos = new THREE.Vector3();
    camera.getWorldPosition(world_camera_pos);

    var world_camera_dir = new THREE.Vector3();
    camera.getWorldDirection(world_camera_dir);

    //UPDATE CAMERA TRANSFORM
    for(var i = 0; i < num_portals; i++)
    {
        var sibling_index = (i + 1) % num_portals;

        var portal_to_update = portals[i];
        var portal_to_see = portals[sibling_index];

        var offset = new THREE.Vector3();
        portal_to_update.mesh.getWorldDirection(offset);
        
        var m_local = new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(0, Math.PI, 0));
        var m = new THREE.Matrix4().multiplyMatrices(portal_to_update.mesh.matrixWorld.clone(), m_local);
        var m_inverse = new THREE.Matrix4().getInverse(portal_to_see.mesh.matrixWorld.clone());

        var p = new THREE.Vector3();
        var r = new THREE.Quaternion();
        var s = new THREE.Vector3();
   
        var m_cam = camera.matrixWorld.clone();
        m_inverse.multiply(m_cam);
        m.multiply(m_inverse);
        
        m.decompose(p, r, s);

        p.add(offset.multiplyScalar(character_width + 0.1))
        portal_to_update.camera.position.copy(p);
        portal_to_update.camera.quaternion.copy(r);

        //update near
        portal_to_update.camera.near = portal_to_update.camera.position.distanceTo(portal_to_update.mesh.position) + 1;
        portal_to_update.camera.updateProjectionMatrix();
    }

    //RENDER
    for(var i = 0; i < num_portals; i++)
    {
        if(!portals[i].active) continue;

        var sibling_index = (i + 1) % num_portals;

        renderer.setRenderTarget(portals[i].buffer);
        renderer.render(scene, portals[sibling_index].camera);
    }
    renderer.setRenderTarget(null);
}

function RegisterCollidingObject(object)
{
    last_obj = object;
    c_timer = 0;
}

function CollisionTimer(delta)
{
    if(last_obj != null)
    {
        c_timer += delta;
        if(c_timer >= max_time)
            last_obj = null;
    }
}

function UpdateResizing(delta)
{
    for(var i = 0; i < portals.length; i++)
    {
        var p = portals[i];
        if(p.resizing == true)
        {
            p.resize_timer += delta;
            var alpha = p.resize_timer / resize_time;
            alpha = Clamp(alpha, 0, 1);

            if(alpha >= 1)
                p.resizing = false;

            p.mesh.scale.lerpVectors(new THREE.Vector3(0,0,0), p.scale, alpha);
        }
    }
}

function PortalsUpdate(camera, scene, delta, character_width)
{
    UpdatePortalsCameras(camera, scene, character_width);
    CollisionTimer(delta);
    UpdateResizing(delta);
}

function OnCollision(other_object, relative_velocity, relative_rotation, contact_normal ) 
{
    if(last_obj == other_object) return;
    if(other_object instanceof Physijs.Mesh)
    {
        var portal = GetPortalFromMesh(this);
        if(portal == undefined) return;
        if(!portal.active) return;
        
        var other_portal = portals[(portal.id + 1) % portals.length];
        if(!other_portal.active) return;
        
        var other_dir = new THREE.Vector3();
        other_portal.mesh.getWorldDirection(other_dir)

        //POSITION
        var pos = other_portal.camera.position.clone();
        pos.add(other_dir.multiplyScalar(0.1));

        //ROTATE
        rot = other_portal.camera.quaternion.clone();

        //CALL CALLBACK
        _onCollision(other_object, pos, rot, portal.mesh.quaternion, other_portal.mesh.quaternion);

        RegisterCollidingObject(other_object);
    }
}

function GetObjectData(object)
{
    if(_onCollisionData == null) return matrixWorld.clone();
    else return _onCollisionData(object);
}

function AddCollisionListener(collisionData, collisionFunction)
{
    _onCollisionData = collisionData;
    _onCollision = collisionFunction;
}

function GetPortalFromMesh(object)
{
    for(var i = 0; i < portals.length; i++)
    {
        if(portals[i].mesh == object)
            return portals[i];
    }
    return null;
}