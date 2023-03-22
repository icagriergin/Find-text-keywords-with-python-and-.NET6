using text_summary.Models.Enums;

namespace text_summary.Models;

public class TextToSummary
{
    public string SourceText { get; set; }
    
    public string SummaryText { get; set; }
    
    public AlgorithmType AlgorithmType { get; set; }
}