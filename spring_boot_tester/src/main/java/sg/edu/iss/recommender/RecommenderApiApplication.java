package sg.edu.iss.recommender;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class })
public class RecommenderApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(RecommenderApiApplication.class, args);

		
		long start = System.currentTimeMillis();
		
		//#### --ML PRIORITY #1-- ###
		new Thread(new Runnable() {
		    public void run() {
		    	HashMap<String, List<String>> recommendMap1 = getLandingSingleRecipeReco("xxx@gmail.com", 10);
		    	printLandingSingleRecipeReco(recommendMap1); //for inspection purposes only
		    }
		}).start();
		
		//#### --ML PRIORITY #2-- ###
		new Thread(new Runnable() {
		    public void run() {
				List<String> recommendList1 = getLandingYouMightLikeReco("xxx@gmail.com", 10);
				printLandingYouMightLikeReco(recommendList1); //for inspection purposes only
		    }
		}).start();
		
		
		long end = System.currentTimeMillis();
		long elapsedTime = end - start;
		
		
		//#### --ML PRIORITY #4-- ###
		List<String> recommendList2 = getMoreLikeThisRecipeReco("6200687714f22c4340f92e15", 10);
		printMoreLikeThisRecipeReco(recommendList2); //for inspection purposes only
		
		//#### --ML PRIORITY #5-- ###
		List<String> predictedDiff = getDifficultyPrediction("6200687714f22c4340f92e15");
		
		long end2 = System.currentTimeMillis();
		long elapsedTime2 = end2 - start;
		
		System.out.println("Elapse Time for Landing Page: " + elapsedTime + " milliseconds");
		System.out.println("Elapse Time for Others: " + elapsedTime2 + " milliseconds");
	}
	
	//######################################### --ML PRIORITY #1-- #############################################
	public static HashMap<String, List<String>> getLandingSingleRecipeReco(String userEmail, int noOfRecommendations) 
	{
		String uriString1 = "http://127.0.0.1:5000/landingSingleRecipeReco?userId=" + userEmail + "&n=" + noOfRecommendations;
		HttpRequest request1 = HttpRequest.newBuilder()
				.uri(URI.create(uriString1))
				.method("GET", HttpRequest.BodyPublishers.noBody())
				.build();
		
		HashMap<String, List<String>> recommendMap = null;
		
		try 
		{
			HttpResponse<String> response1 = HttpClient.newHttpClient().send(request1, HttpResponse.BodyHandlers.ofString());
			if (response1!= null) {
				JSONObject jo = (JSONObject) new JSONParser().parse(response1.body());
				String receivedUserId = (String) jo.get("userId");
				String queryRecipeId = (String) jo.get("query_recipeID");
				ArrayList<String> recommendList = (ArrayList<String>) jo.get("recommendations");
				
				recommendMap = new HashMap<>();
				recommendMap.put("queryRecipeId", new ArrayList<>(Arrays.asList(queryRecipeId)));
				recommendMap.put("recommendList", recommendList);
				
				System.out.println("===========API PRIORITY #1: Landing Page SINGLE_RECIPE RECOS=================");
				System.out.println("API Resp1 Status: \t" + response1.statusCode());
				System.out.println("Source1 API URL: \t" + response1.uri().toString());
				System.out.println("UserId (email): \t" + receivedUserId);
			}
		}
		catch (Exception e) {
				System.out.println("There was a connection error");
		}
		
		return recommendMap;
		
	}
	
	public static void printLandingSingleRecipeReco(HashMap<String, List<String>> recommendMap) {
		
		System.out.println("***PRINT RESULT: LANDING PAGE - SINGLE_RECIPE RECOS***");
		System.out.println("Query RecipeID: \t" + recommendMap.get("queryRecipeId").get(0));
		System.out.println("");
		List<String> recommendList = recommendMap.get("recommendList");
		if (recommendList != null)
			recommendList.stream().map(x -> "Recommended RecipeID:\t" + x).forEach(System.out::println);
		else
			System.out.println("RecommendList is null");
	}
	
	//######################################### --ML PRIORITY #2-- #############################################
	public static List<String> getLandingYouMightLikeReco(String userEmail, int noOfRecommendations) 
	{
		String uriString1 = "http://127.0.0.1:5000/landingYouMightLikeReco?userId=" + userEmail + "&n=" + noOfRecommendations;
		HttpRequest request1 = HttpRequest.newBuilder()
				.uri(URI.create(uriString1))
				.method("GET", HttpRequest.BodyPublishers.noBody())
				.build();
		
		List<String> recommendList = null;
		
		try 
		{
			HttpResponse<String> response1 = HttpClient.newHttpClient().send(request1, HttpResponse.BodyHandlers.ofString());
			if (response1!= null) {
				JSONObject jo = (JSONObject) new JSONParser().parse(response1.body());
				String receivedUserId = (String) jo.get("userId");
				recommendList = (ArrayList<String>) jo.get("recommendations");
				
				
				System.out.println("===========API PRIORITY #2: Landing Page YOU MIGHT LIKE RECOS=================");
				System.out.println("API Resp1 Status: \t" + response1.statusCode());
				System.out.println("Source1 API URL: \t" + response1.uri().toString());
				System.out.println("UserId (email): \t" + receivedUserId);
			}
		}
		catch (Exception e) {
				System.out.println("There was a connection error");
		}
		
		return recommendList;
		
	}
	
	public static void printLandingYouMightLikeReco(List<String> recommendList) {
		
		System.out.println("***PRINT RESULT: LANDING PAGE - YOU MIGHT LIKE RECOS****");
		if (recommendList != null)
			recommendList.stream().map(x -> "Recommended RecipeID:\t" + x).forEach(System.out::println);
		else
			System.out.println("RecommendList is null");
	}
	
	
	
	
	
	//######################################### --ML PRIORITY #4-- #############################################
	public static List<String> getMoreLikeThisRecipeReco(String recipeId, int noOfRecommendations) 
	{
		String uriString1 = "http://127.0.0.1:5000/moreLikeThisReco?recipeId=" + recipeId + "&n=" + noOfRecommendations;
		HttpRequest request1 = HttpRequest.newBuilder()
				.uri(URI.create(uriString1))
				.method("GET", HttpRequest.BodyPublishers.noBody())
				.build();
		
		List<String> recommendList = null;
		
		try 
		{
			HttpResponse<String> response1 = HttpClient.newHttpClient().send(request1, HttpResponse.BodyHandlers.ofString());
			if (response1!= null) {
				JSONObject jo = (JSONObject) new JSONParser().parse(response1.body());
				String receivedUserId = (String) jo.get("userId");
				recommendList = (ArrayList<String>) jo.get("recommendations");
				
				
				System.out.println("===========API PRIORITY #4: MORE LIKE THIS RECIPE RECOS=================");
				System.out.println("API Resp1 Status: \t" + response1.statusCode());
				System.out.println("Source1 API URL: \t" + response1.uri().toString());
		
			}
		}
		catch (Exception e) {
				System.out.println("There was a connection error");
		}
		
		return recommendList;
		
	}
	
	public static void printMoreLikeThisRecipeReco(List<String> recommendList) {
		
		System.out.println("***PRINT RESULT: MORE LIKE THIS RECOS****");
		if (recommendList != null)
			recommendList.stream().map(x -> "Recommended RecipeID:\t" + x).forEach(System.out::println);
		else
			System.out.println("RecommendList is null");
	}
	
	
	//######################################### --ML PRIORITY #5-- #############################################
	public static List<String> getDifficultyPrediction(String recipeId) 
	{
		String uriString1 = "http://127.0.0.1:5000/predictDifficulty?recipeId=" + recipeId;
		HttpRequest request1 = HttpRequest.newBuilder()
				.uri(URI.create(uriString1))
				.method("GET", HttpRequest.BodyPublishers.noBody())
				.build();
		
		List<String> prediction = null;
		
		try 
		{
			HttpResponse<String> response1 = HttpClient.newHttpClient().send(request1, HttpResponse.BodyHandlers.ofString());
			if (response1!= null) {
				JSONObject jo = (JSONObject) new JSONParser().parse(response1.body());
				prediction = (ArrayList<String>) jo.get("prediction");
				
				System.out.println("===========API PRIORITY #5: Difficulty Tag Prediction=================");
				System.out.println("API Resp Status: \t" + response1.statusCode());
				System.out.println("Source API URL: \t" + response1.uri().toString());
				System.out.println("Difficulty prediction: \t" + prediction.get(0));
			}
		}
		catch (Exception e) {
				System.out.println("There was a connection error");
		}
		
		return prediction;
		
	}
	
	
	
	
	
	//# --Old tests-- #
	public static void testFlaskApi(int x1, int x2) 
	{
		String uriString1 = "http://127.0.0.1:5000/model1?x=" + x1;
		
		HttpRequest request1 = HttpRequest.newBuilder()
				.uri(URI.create(uriString1))
				.method("GET", HttpRequest.BodyPublishers.noBody())
				.build();
		
		
		String uriString2 = "http://127.0.0.1:5000/model2?x=" + x2;
		
		HttpRequest request2 = HttpRequest.newBuilder()
				.uri(URI.create(uriString2))
				.method("GET", HttpRequest.BodyPublishers.noBody())
				.build();
		
		try 
		{
			HttpResponse<String> response1 = HttpClient.newHttpClient().send(request1, HttpResponse.BodyHandlers.ofString());
			HttpResponse<String> response2 = HttpClient.newHttpClient().send(request2, HttpResponse.BodyHandlers.ofString());
			if (response1!= null && response2!= null) 
			{
				
				//Model 2-------------------
				
				
				String result1 = (String) response1.body().toString();
				
				System.out.println("===========MODEL 1===================");
				System.out.println("API Resp1 Status: \t" + response1.statusCode());
				System.out.println("Source1 API URL: \t" + response1.uri().toString());
				System.out.println("API Input1: \t\t" + x1);
				System.out.println("API Result1: \t\t" + result1);
				
				//Model 2-------------------
				
				
				String result2 = (String) response2.body().toString();
				
				System.out.println("===========MODEL 2===================");
				System.out.println("API Resp2 Status: \t" + response2.statusCode());
				System.out.println("Source2 API URL: \t" + response2.uri().toString());
				System.out.println("API Input2: \t\t" + x2);
				System.out.println("API Result2: \t\t" + result2);
				
			}
		}
		catch (Exception e) 
		{
				System.out.println("There was a connection error");
		}
		
	}
		
	public static void testApi() {
		System.out.println("Trying out Test API");
		HttpRequest request = HttpRequest.newBuilder()
				.uri(URI.create("https://yummly2.p.rapidapi.com/feeds/list?start=0&limit=18&tag=list.recipe.popular"))
				.header("x-rapidapi-host", "yummly2.p.rapidapi.com")
				.header("x-rapidapi-key", "91082ada61msh47b4a99007a25f8p17b117jsnc919172a977e")
				.method("GET", HttpRequest.BodyPublishers.noBody())
				.build();
		
		try {
			HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
			if (response!= null) {
				System.out.println("Response Status Code: " + response.statusCode());
				System.out.println("Source API URL: " + response.uri().toString());
				
		        Object obj = new JSONParser().parse(response.body());
		          
		        // typecasting obj to JSONObject
		        JSONObject jo = (JSONObject) obj;
		        JSONArray  feed = (JSONArray) jo.get("feed");
		        
		        for (Object o: feed) {
		        	JSONObject cjo = (JSONObject) o;
			        Object display = cjo.get("display");
			        JSONObject displayjo = (JSONObject) display;
			        String displayName = (String) displayjo.get("displayName");
		        	System.out.println("Recipe Title: " + displayName);
		        }
		        
				
				
				System.out.println("done with response body");
			}
				
			
		}
		catch (Exception e) {
			System.out.println("There was a connection error");
		}
	}

}
