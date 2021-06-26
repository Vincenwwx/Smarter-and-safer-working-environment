(define (domain office)
  (:requirements  :strips  :typing  :negative-preconditions  :disjunctive-preconditions )
  (:types
   room fan light message  - object
   )
   
    (:predicates
          
          (comfortable-temp)
          (light-sufficient)
          
         
         
          (on1 ?l - light)
          (off1 ?l - light)
          
          (on2 ?f - fan)
          (off2 ?f - fan)
         
          
          
          
          (at-light ?l - light ?r - room)
          (at-fan ?f - fan ?r - room)
          
    
          (send ?m - message)
          

   )

   (:functions
    
	  (temp ?r - room)
	  (light ?r - room)
	  (humidity ?r - room)
	  (bodytemp_limit)
	  (temp_limit)
	  (light_limit)
	  (humidity_limit)
   )
	  
  
    
    
   (:action switchoff_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (and (on1 ?l) (>(light ?r) (light_limit)))
        :effect (and(not(on1 ?l)) (send ?m) (light-sufficient))
   )
   
   (:action switchon_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (or (not(on1 ?l)) (<(light ?r) (light_limit)))
        :effect (and (on1 ?l) (send ?m) (light-sufficient))
   )
   
   
   

        
   (:action switchoff_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (and (on2 ?f) (>(temp ?r) (temp_limit)) (>(humidity ?r) (humidity_limit)))
        :effect (and(not(on2 ?f)) (send ?m) (comfortable-temp))
   )
   
   (:action switchon_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (or (not(on2 ?f)) (<(temp ?r) (temp_limit)) (<(humidity ?r) (humidity_limit)))
        :effect (and (on2 ?f) (send ?m) (comfortable-temp))
   ))