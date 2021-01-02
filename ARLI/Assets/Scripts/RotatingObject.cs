using UnityEngine;

public class RotatingObject : MonoBehaviour
{
    public float xAngle, yAngle, zAngle, speed;
   
    void Update()
    {
        transform.Rotate(xAngle*speed, yAngle*speed, zAngle*speed);
    }
}
