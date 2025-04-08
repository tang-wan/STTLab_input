def initialize(): 
    global Path
    global Ntot
    global run
    global NLL_list
    global spec_NL_set
    global spec_NL
    global init_Angle
    global finl_Angle
    global sep_Angle
    global γLI_Angle
    global γR_Angle
    
    run  = 1
    ## False (0): Just create the film, don't auto submit the job
    ## True  (1): Create the film and auto submit the job

    Path = 0
    ## False (0): Don't print the detail of the path
    ## True  (1): Print the detail of the path

    Ntot = 9
    NLL_list  = [9, 8]

    spec_NL_set = "ALL"                     # Run all the NLL set
    # spec_NL_set = (2, 2, 1, 1, 1, 1, 1)     # Run the specific NLL set
    spec_NL = "ALL"                     # Run all the combination of this NLL
    # spec_NL = (3, 1, 1, 1, 1, 1, 1)     # Run the specific combination of this NLL

    init_Angle = 0  # The initial angle of γL iteration (unit: degree)
    finl_Angle = 90  # The final angle of γL iteration (unit: degree)
    sep_Angle  = 45  # The angle interval of γL iteration (unit: degree)
    ## If init_Angle and finl_Angle are the same, which mean running the specific angle of γL

    γLI_Angle, γR_Angle = (180, 0)  # Setting the γLI and γR
