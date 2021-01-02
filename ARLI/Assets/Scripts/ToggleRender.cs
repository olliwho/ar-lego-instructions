using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ToggleRender : MonoBehaviour
{
	public bool visible = true;

	public void ToogleVisibility()
	{
		Renderer rend = gameObject.GetComponent<Renderer>();
		
		if(visible)
			rend.enabled = false;
		else
			rend.enabled = true;
	}

	private void Update()
	{
		Renderer rend = gameObject.GetComponent<Renderer>();

		if (visible)
			rend.enabled = true;
		else
			rend.enabled = false;
	}
}
