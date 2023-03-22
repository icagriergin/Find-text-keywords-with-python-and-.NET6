using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Mvc;
using text_summary.Models;
using text_summary.Models.Enums;
using text_summary.Models.ViewModels;
namespace text_summary.Controllers;

public class HomeController : Controller
{
    private readonly IHttpClientFactory _httpClientFactory;

    public HomeController(IHttpClientFactory httpClientFactory) =>
        _httpClientFactory = httpClientFactory;

    private const string baseUrl = "http://127.0.0.1:5001/";
    
    public IActionResult Index()
    {
        return View();
    }

    [HttpPost]
    public JsonResult GetKeywordsFromText(string sourceText, AlgorithmType algorithmTypeValue)
    {
        if (string.IsNullOrWhiteSpace(sourceText))
            return Json(null);

        switch (algorithmTypeValue)
        {
            case AlgorithmType.YakeAlgorithm:
                return Json(RunYakeAlgorithm(sourceText));
                break;
            
            case AlgorithmType.Keybert:
                return Json(RunKeybertAlgorithm(sourceText));
                break;
            
            case AlgorithmType.TextRank4ZhAlgorithm:
                return Json(RunTextRank4ZhAlgorithm(sourceText));
                break;
            
            case AlgorithmType.RakunAlgorithm:
                return Json(RunRakunAlgorithm(sourceText));
                break;
            
            case AlgorithmType.PurePythonExtractorAlgorithm:
                return Json(RunPurePythonExtractor(sourceText));
                break;
        }
        
        return Json(null);
    }

    private TextToSummary RunPurePythonExtractor(string sourceText)
    {
        var result = MakeHttpRequest(sourceText,baseUrl+"runPurePythonExtractor").Result;
        var response = JsonSerializer.Deserialize<TextToSummary>(result);
        
        return response;
    }
    
    private TextToSummary RunYakeAlgorithm(string sourceText)
    {
        var result = MakeHttpRequest(sourceText,baseUrl+"runYakeAlgorithm").Result;
        var response = JsonSerializer.Deserialize<TextToSummary>(result);
        
        return response;
    }
    
    private TextToSummary RunKeybertAlgorithm(string sourceText)
    {
        var result = MakeHttpRequest(sourceText,baseUrl+"runKeybertAlgorithm").Result;
        var response = JsonSerializer.Deserialize<TextToSummary>(result);
        
        return response;
    }
    
    private TextToSummary RunTextRank4ZhAlgorithm(string sourceText)
    {
        
        var result = MakeHttpRequest(sourceText,baseUrl+"runTextRank4ZhAlgorithm").Result;
        var response = JsonSerializer.Deserialize<TextToSummary>(result);
        
        return response;
    }
    
    private TextToSummary RunRakunAlgorithm(string sourceText)
    {
        var result = MakeHttpRequest(sourceText,baseUrl+"runRakunAlgorithm").Result;
        var response = JsonSerializer.Deserialize<TextToSummary>(result);
        
        return response;
    }
    
    private async Task<string> MakeHttpRequest(string sourceText,string url)
    {
        using StringContent jsonContent = new(
            JsonSerializer.Serialize(new
            {
                SourceText = sourceText
            }),
            Encoding.UTF8,
            "application/json");
        
        var httpClient = _httpClientFactory.CreateClient();
        
        using HttpResponseMessage response = await httpClient.PostAsync(
            url,
            jsonContent);

        var jsonResponse = await response.Content.ReadAsStringAsync();
        return jsonResponse;
    }
}