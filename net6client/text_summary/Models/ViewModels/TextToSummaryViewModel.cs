using text_summary.Models.Enums;

namespace text_summary.Models.ViewModels;

public class TextToSummaryViewModel
{
    public string SourceText { get; set; }
    
    public string SummaryText { get; set; }
    
    public AlgorithmType AlgorithmType { get; set; }
}