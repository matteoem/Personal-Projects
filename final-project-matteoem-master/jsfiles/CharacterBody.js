
var character_body;

function CreateBody(model, camera)
{
    character_body = { model:model, camera:camera };
}

function UpdateBody(delta)
{
    SetPosition();
    SetRotation();
}

function SetPosition()
{
    character_body.model.position.copy(character_body.camera.position);
}

function SetRotation()
{
    var euler = new THREE.Euler( 0, 0, 0, 'YXZ' );
    euler.setFromQuaternion( character_body.camera.quaternion );
    euler.z = euler.x = 0;
    character_body.model.quaternion.setFromEuler(euler);
}