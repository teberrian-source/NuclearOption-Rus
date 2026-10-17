using UnityEngine;

namespace KoreanPatch;

internal class FrameHelper : MonoBehaviour
{
	private void Update()
	{
		Plugin.Instance?.DoPerFrameLogic();
	}
}
