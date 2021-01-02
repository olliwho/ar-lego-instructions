using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;
using Microsoft.MixedReality.Toolkit.Input;
using Microsoft.MixedReality.Toolkit.UI;
using System.Collections;
using UnityEngine.Networking;
using System.IO;
using System.Linq;
using System;

public class ModelPicker : MonoBehaviour
{

    private string model_name = "Pyramid";
    private GameObject model = null;

    // Start is called before the first frame update
    void Start()
    {
        ShowModelPicker(true);
        //Test();
    }

    // Update is called once per frame
    void Update()
    {
        Dropdown dropdown = gameObject.transform.Find("Canvas").Find("Dropdown").gameObject.GetComponent<Dropdown>();
        model_name = dropdown.options[dropdown.value].text;
    }

    public void ShowModelPicker(bool start = false)
    {
        GameObject camera = gameObject.transform.Find("Main Camera").gameObject;
        GameObject camera_canvas = camera.transform.Find("Canvas").gameObject;
        //make camera canvas invisible
        camera_canvas.SetActive(false);

        // remove model if we come back from instructions
        if (!start)
        {
            Destroy(gameObject.transform.GetChild(gameObject.transform.childCount - 1).gameObject);
            gameObject.transform.Find("Canvas").gameObject.SetActive(true);

            //Destroy small model
            Destroy(camera_canvas.transform.GetChild(1).gameObject);
            model = null;
        }
        else
        {
            List<string> dd_options = new List<string>();

            var myLoadedAssetBundle = AssetBundle.LoadFromFile(Path.Combine("file:///", Application.streamingAssetsPath, "models"));
            if (myLoadedAssetBundle == null)
            {
                Debug.Log("Failed to load AssetBundle!");
                return;
            }
            TextAsset models_file = myLoadedAssetBundle.LoadAsset<TextAsset>("models");

            string[] model_names = models_file.ToString().Split('\n');
            foreach (string model_name in model_names)
            {
                if (model_name.Length == 0)
                    continue;
                dd_options.Add((model_name).Trim());
            }

            Dropdown dropdown = gameObject.transform.Find("Canvas").Find("Dropdown").gameObject.GetComponent<Dropdown>();
            dropdown.AddOptions(dd_options);
        }

        //var options = playspace.transform.GetChild(1).gameObject.transform.GetChild(1).gameObject.GetComponent<Dropdown>().options;
        //model_name = options[Random.Range(0, options.Count)].text;
        //model_name = "21008-1 - Burj Khalifa";
        //LoadObject();
    }

    public void LoadObject()
    {
        GameObject playspace = this.gameObject;
        GameObject camera = playspace.transform.Find("Main Camera").gameObject;
        model = new GameObject(model_name);
        model.transform.parent = playspace.transform;
        model.AddComponent<MeshRenderer>();
        model.AddComponent<StepToggle>();


        Vector3 camera_pos = camera.transform.position;
        Vector3 camera_dir = camera.transform.forward;
        model.transform.position = camera_pos + camera_dir;
        model.transform.position += new Vector3(0.0f, -0.05f, 0.6f);
        model.transform.localScale = new Vector3(0.0005f, 0.0005f, 0.0005f);

        AssetBundle.UnloadAllAssetBundles(true);
        var myLoadedAssetBundle = AssetBundle.LoadFromFile(Path.Combine("file:///", Application.streamingAssetsPath, model_name));
        if (myLoadedAssetBundle == null)
        {
            Debug.Log("Failed to load AssetBundle!");
            return;
        }
        var fileArray = myLoadedAssetBundle.LoadAllAssets<GameObject>();
        foreach (var obj in fileArray)
        {
            if (obj.name.Contains("step"))
            {
                GameObject step_model = Instantiate(obj);
                step_model.transform.parent = model.transform;
                //get step number to set the right order
                int step_num = int.Parse(string.Join("", obj.name.Substring(obj.name.IndexOf("step")).ToCharArray().Where(Char.IsDigit)));
                step_model.transform.SetSiblingIndex(step_num);
                //AddLines(step_model);
                step_model.transform.localPosition = new Vector3(0.0f, 0.0f, 0.0f);
                step_model.transform.localScale = new Vector3(1.0f, 1.0f, 1.0f);
                step_model.transform.GetChild(0).gameObject.AddComponent<StepHighlighter>();
            }
            else if (obj.name.Equals(model_name) || obj.name.Equals(model_name.ToLower()))
            {
                GameObject model_small = Instantiate(obj);
                model_small.transform.parent = camera.transform.GetChild(1).gameObject.transform;
                //AddLines(model_small);
                model_small.transform.localPosition = new Vector3(0f, -6.7f, -0.7f);
                model_small.transform.localRotation = new Quaternion(0.165f, -73.45901f, 31.383f, 0);
                model_small.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);

                float canvas_width = model_small.transform.parent.GetComponent<RectTransform>().rect.width * model_small.transform.parent.GetComponent<RectTransform>().transform.localScale.x;
                float bb_width = model_small.transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().bounds.size.x * 2.25f;

                model_small.transform.localScale = new Vector3(canvas_width / bb_width, canvas_width / bb_width, canvas_width / bb_width);

                RotatingObject ro = model_small.AddComponent<RotatingObject>();
                ro.yAngle = 2;
                ro.speed = 0.2f;
            }
            else
            {
                //bricks.Add(obj.name, obj);
            }
        }

        // make small model canvas visible
        camera.transform.Find("Canvas").gameObject.SetActive(true);
        // make model picker menu invisible
        playspace.transform.Find("Canvas").gameObject.SetActive(false);

        ConfigSpeechInputHandler();

        // add components to move and scale the model
        ManipulationHandler mh = model.AddComponent<ManipulationHandler>();
        ManipulationHandler.ReleaseBehaviorType ReleaseBehaviorType = ManipulationHandler.ReleaseBehaviorType.KeepVelocity & ManipulationHandler.ReleaseBehaviorType.KeepAngularVelocity;
        mh.ReleaseBehavior = ReleaseBehaviorType;
        model.AddComponent<BoundingBox>();
        Rigidbody modelRigidBody = model.AddComponent<Rigidbody>();
        modelRigidBody.useGravity = false;
        model.AddComponent<NearInteractionGrabbable>();
    }

    void AddLines(GameObject parent)
    {
        GameObject lines_obj = new GameObject("Lines");
        lines_obj.transform.parent = parent.transform;
        lines_obj.transform.localPosition = new Vector3(0.0f, 0.0f, 0.0f);

        string file_name = model_name + "/" + parent.name.ToLower().Replace("(clone)", "") + "_lines";
        TextAsset lines_file = Resources.Load(file_name) as TextAsset;
        string[] lines = lines_file.ToString().Split('\n');

        //create line per 3 lines in file

        List<Vector3> vertices = new List<Vector3>();
        foreach (string line in lines)
        {
            string[] l = line.Split(' ');
            switch (l[0])
            {
                case "v":
                    vertices.Add(new Vector3(float.Parse(l[1]), float.Parse(l[2]), float.Parse(l[3])));
                    break;
                case "l":
                    CreateLine(lines_obj, vertices.ToArray());
                    vertices.Clear();
                    break;
                default:
                    break;
            }
        }
    }

    void CreateLine(GameObject lines_obj, Vector3[] vertices)
    {
        GameObject line = new GameObject("line");
        line.transform.parent = lines_obj.transform;
        line.transform.localPosition = new Vector3(0.0f, 0.0f, 0.0f);
        line.AddComponent<LineRenderer>();
        LineRenderer lr = line.GetComponent<LineRenderer>();
        lr.material = new Material(Shader.Find("Sprites/Default"));
        lr.startWidth = 0.001f;
        lr.startColor = new Color(0.0f, 0.0f, 0.0f);
        lr.endColor = new Color(0.0f, 0.0f, 0.0f);
        lr.SetPositions(vertices);
        lr.useWorldSpace = false;
    }

    public void Drop()
    {
        Rigidbody rig = model.GetComponent<Rigidbody>();
        rig.useGravity = true;
    }

    public void ModelReturn()
    {
        Rigidbody rig = model.GetComponent<Rigidbody>();
        rig.useGravity = false;
        rig.velocity = new Vector3(0f, 0f, 0f);
        rig.angularVelocity = new Vector3(0f, 0f, 0f);

        GameObject camera = gameObject.transform.Find("Main Camera").gameObject;
        Vector3 camera_pos = camera.transform.position;
        Vector3 camera_dir = camera.transform.forward;
        model.transform.position = camera_pos + camera_dir;
        model.transform.position += new Vector3(0.0f, -0.07f, 0.5f);
        model.transform.rotation = Quaternion.Euler(new Vector3(0f, 0f, 0f));
    }

    void ConfigSpeechInputHandler()
    {
        SpeechInputHandler sih = GetComponent<SpeechInputHandler>();

        UnityAction action = model.GetComponent<StepToggle>().NextStep;
        sih.AddResponse("Next", action);

        action = model.GetComponent<StepToggle>().LastStep;
        sih.AddResponse("Last", action);

        action = GetComponent<ModelPicker>().Drop;
        sih.AddResponse("Drop", action);

        action = GetComponent<ModelPicker>().ModelReturn;
        sih.AddResponse("Come Back", action);
    }










    void Test()
    {
        var myLoadedAssetBundle = AssetBundle.LoadFromFile(Path.Combine(Application.dataPath, "AssetBundles/models"));
        if (myLoadedAssetBundle == null)
        {
            Debug.Log("Failed to load AssetBundle!");
            return;
        }
        TextAsset models = myLoadedAssetBundle.LoadAsset<TextAsset>("models");

        string[] model_names = models.ToString().Split('\n');


        foreach (string model in model_names)
        {
            string model_name = model.ToLower().Trim();
            myLoadedAssetBundle = AssetBundle.LoadFromFile(Path.Combine(Application.dataPath, "AssetBundles", model_name));
            if (myLoadedAssetBundle == null)
            {
                Debug.Log("Failed to load AssetBundle!");
                return;
            }

            var objs = myLoadedAssetBundle.LoadAllAssets<GameObject>();

            foreach (var obj in objs)
            {
                Debug.Log(obj.name);
            }
            /*            GameObject model_small = myLoadedAssetBundle.LoadAsset<GameObject>(model_name);
                        model_small = Instantiate(model_small);
                        model_small.transform.parent = transform.Find("Main Camera").Find("Canvas").gameObject.transform;

                        model_small.transform.localPosition = new Vector3(0f, -6.7f, -0.7f);
                        model_small.transform.localRotation = new Quaternion(0.165f, -73.45901f, 31.383f, 0);
                        model_small.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);

                        float canvas_width = model_small.transform.parent.GetComponent<RectTransform>().rect.width * model_small.transform.parent.GetComponent<RectTransform>().transform.localScale.x;
                        float bb_width = model_small.transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().bounds.size.x * 2.25f;

                        model_small.transform.localScale = new Vector3(canvas_width / bb_width, canvas_width / bb_width, canvas_width / bb_width);

                        RotatingObject ro = model_small.AddComponent<RotatingObject>();
                        ro.yAngle = 2;
                        ro.speed = 0.2f;*/

            /*
                        GameObject step_model = myLoadedAssetBundle.LoadAsset<GameObject>(model_name+"_step0");
                        if (step_model == null)
                        {
                            Debug.Log("Failed to load AssetBundle model!");
                            return;
                        }
                        step_model = Instantiate(step_model);
                        step_model.transform.parent = transform.Find("Main Camera").Find("Canvas").gameObject.transform;
                        //AddLines(step_model);
                        step_model.transform.localPosition = new Vector3(0.0f, 0.0f, 0.0f);
                        step_model.transform.localScale = new Vector3(1.0f, 1.0f, 1.0f);
                        step_model.transform.GetChild(0).gameObject.AddComponent<StepHighlighter>();*/

        }

    }

}
