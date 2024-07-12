from source.manager.asset import ImgIcon, Area, Text, LOG_WHEN_TRUE, Button

IconGeneralChallengeSuccess = ImgIcon(threshold=0.99, print_log=LOG_WHEN_TRUE)
ButtonDomainFailure = Button(threshold=0.98)
ButtonDomainRetry = Button(threshold=0.98)
AreaDomainFailure = Area()
TextDomainExit = Text(zh='退出秘境',cap_area=AreaDomainFailure.position)
TextDomainRechallenge = Text(zh='再次挑战',cap_area=AreaDomainFailure.position)