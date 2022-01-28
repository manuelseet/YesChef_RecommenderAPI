package sg.edu.iss.recommender;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

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
		testApi();

		
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
