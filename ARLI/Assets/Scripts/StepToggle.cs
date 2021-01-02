using UnityEngine;

public class StepToggle : MonoBehaviour
{
    public int step = 1;

    void Start()
    {
        int count = gameObject.transform.childCount;


        for (int i = 1; i < count; i++)
        {
            gameObject.transform.GetChild(i).gameObject.SetActive(false);
        }
        StepHighlighter sh = gameObject.transform.GetChild(0).gameObject.transform.GetChild(0).gameObject.GetComponent<StepHighlighter>();
        sh.activeStep = true;
    }

    void CheckStep()
    {
        int count = gameObject.transform.childCount - 1;
        if(step > count)
            step = count;
        if (step < 0)
            step = 0;
    }

    public void NextStep()
    {
        step++;
        CheckStep();
        SetStepsVisible();
    }

    public void LastStep()
    {
        step--;
        CheckStep();
        SetStepsVisible();
    }

    void SetStepsVisible()
    {
        int count = gameObject.transform.childCount - 1;
        for (int i = 0; i < count; i++)
        {
            if (i < step)
            {
                gameObject.transform.GetChild(i).gameObject.SetActive(true);
                if (i == (step - 2))
                {
                    StepHighlighter sh = gameObject.transform.GetChild(i).gameObject.transform.GetChild(0).gameObject.GetComponent<StepHighlighter>();
                    sh.activeStep = false;
                }
                if (i == (step-1))
                {
                    StepHighlighter sh = gameObject.transform.GetChild(i).gameObject.transform.GetChild(0).gameObject.GetComponent<StepHighlighter>();
                    sh.activeStep = true;
                }
            }
            else
            {
                gameObject.transform.GetChild(i).gameObject.SetActive(false);
            }
        }
        //this_go.transform.parent.transform.GetComponent<ModelPicker>().StepChange(step);
    }
}
