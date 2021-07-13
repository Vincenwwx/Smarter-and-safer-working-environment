(define (domain office)
  (:requirements   :strips  :typing  :negative-preconditions :disjunctive-preconditions :fluents :equality :conditional-effects)
  (:types
   room buzzer buzzer1 person light fan heater message  - object
   )
   
    (:predicates
          
          (comfortable-temperature)
          (brightness-sufficient)
          (bodytempcheck-performed)
          (person-detected)
          (off ?l - light)
          (off1 ?f - fan)
          (off2 ?h - heater)
          (off3 ?b - buzzer)
          (off4 ?b1 - buzzer1)
          (at-light ?l - light  ?r - room)
          (at-fan ?f - fan ?r - room)
          (at-heater ?h - heater ?r - room)
          (at-buzzer ?b - buzzer ?p - person)
          (at-buzzer1 ?b1 - buzzer1 ?p - person)
          (send ?m - message)     
    )

   (:functions
    
	  (temp ?r - room)
	  (lightintensity ?r - room)
	  (humidity ?r - room)
	  (bodytemp ?p - person)
	  (motion ?p - person)
	  (temp_limit)
	  (humidity_limit)
	  (lightintensity_limit)
	  (bodytemp_limit)
	  (motion_value)
   )
	  
  
  ; automatic brightness control in the office


   
   (:action switchoff_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (and (off ?l) (>(lightintensity ?r) (lightintensity_limit)))
        :effect (and (not(off ?l)) (send ?m) (brightness-sufficient))
    )

    (:action switchon_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (or (not(off ?l)) (<(lightintensity ?r) (lightintensity_limit)))
        :effect (and (off ?l) (send ?m) (brightness-sufficient))
    )
   
   
   
   ; automatic ventilator control in the office

     
       
   (:action switchoff_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (and (off1 ?f) (<(temp ?r) (temp_limit)) (<(humidity ?r) (humidity_limit)))
        :effect (and(not(off1 ?f)) (send ?m) (comfortable-temperature))
   )
   
   (:action switchon_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (or (not(off1 ?f)) (>(temp ?r) (temp_limit)) (>(humidity ?r) (humidity_limit)))
        :effect (and (off1 ?f) (send ?m) (comfortable-temperature))
   )
   


   ; automatic heater valve control in the office



    (:action switchoff_heater
        :parameters (?h - heater ?r - room ?m - message)
        :precondition (and (off2 ?h) (>(temp ?r) (temp_limit)) (>(humidity ?r) (humidity_limit)))
        :effect (and(not(off2 ?h)) (send ?m) (comfortable-temperature))
     )
   
    (:action switchon_heater
        :parameters (?h - heater ?r - room ?m - message)
        :precondition (or (not(off2 ?h)) (<(temp ?r) (temp_limit)) (<(humidity ?r) (humidity_limit)))
        :effect (and (off2 ?h) (send ?m) (comfortable-temperature))
     )
   
   
    ; automatic bodytemp check in front of the office



    (:action switchoff_buzzer
        :parameters (?b - buzzer ?p - person ?m - message)
        :precondition (and (off3 ?b) (<(bodytemp ?p) (bodytemp_limit))) 
        :effect (and(not(off3 ?b)) (send ?m) (bodytempcheck-performed))
     )
   
     (:action switchon_buzzer
        :parameters (?b - buzzer ?p - person ?m - message)
        :precondition (or (not(off3 ?b)) (>(bodytemp ?p) (bodytemp_limit)))
        :effect (and (off3 ?b) (send ?m) (bodytempcheck-performed))
     )    

     ; ir sesnsor to detect person movement

    (:action switchoff_buzzer1
        :parameters (?b1 - buzzer1 ?p - person ?m - message)
        :precondition (and (off4 ?b1) (<(motion ?p) (motion_value))) 
        :effect (and(not(off4 ?b1)) (send ?m) (person-detected))
     )
   
     (:action switchon_buzzer1
        :parameters (?b1 - buzzer1 ?p - person ?m - message)
        :precondition (or (not(off4 ?b1)) (>=(motion ?p) (motion_value)))
        :effect (and (off4 ?b1) (send ?m) (person-detected))
     )    
)
