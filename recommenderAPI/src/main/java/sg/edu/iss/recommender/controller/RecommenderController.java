package sg.edu.iss.recommender.controller;

import java.time.LocalDate;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@CrossOrigin(origins= "http://localhost:3030") //using different port number
@RestController
@RequestMapping(path="/api")
public class RecommenderController {
	
	//autowire from services here

	@GetMapping("/userRecommends/{userId}")
	public ResponseEntity<?> getUserRecommendations (@PathVariable("userId") int userId) {

		//retrieve from services here... 
		
		
		/*
		if (!userRecoList.isEmpty()) {
			return new ResponseEntity<>(userRecoList, HttpStatus.OK);
		} else {
			return new ResponseEntity<>(HttpStatus.NOT_FOUND);
		}
		*/
		
		return new ResponseEntity<>(HttpStatus.NOT_FOUND);
	}
	
	@GetMapping("/ingredientRecommends/") //must reconsider mapping
	public ResponseEntity<?> getIngredientListRecommendation (@PathVariable("userId") int userId) {

		//retrieve from services here... 
		
		
		/*
		if (!ingredientRecoList.isEmpty()) {
			return new ResponseEntity<>(ingredientRecoList, HttpStatus.OK);
		} else {
			return new ResponseEntity<>(HttpStatus.NOT_FOUND);
		}
		*/
		
		return new ResponseEntity<>(HttpStatus.NOT_FOUND);
	}
	
}
