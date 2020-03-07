# DukeDidi---The ride sharing web-app based on Django

**Team members:**

**Kefan Lin(kl352)**

**Jiateng Mao(jm668)**

****

DukeDidi is a Django web-app which let users request, drive for, and join rides. It satisfies all the requirements specified in the Excel form. 



## URL Layout and Description

- Log-in : http://vcm-12439.vm.duke.edu:8000/DukeDidi/login/
  - In this page, user can either log in to the app, or register as a new user. This website is able to handle login failure with an an invalid user account.
- User register : http://vcm-12439.vm.duke.edu:8000/DukeDidi/dashboard
  - Unregistered user can register in this page using his/her email address. The password is encrypted with a salt using SHA1 algorithm. Then the encrypted(password+salt) with salt will be stored in the database together.

- Ride request (ride owner): http://vcm-12439.vm.duke.edu:8000/DukeDidi/requestRide/
  - A logged-in user can request a ride in this page by specifying the destination, arrival time, party size, is sharable or not, and vehicle type.

- Search sharable rides (ride sharer) : http://vcm-12439.vm.duke.edu:8000/DukeDidi/searchSharableRides
  - A logged-in user can search sharable rides by specifying the destination, arrival time window, and party size.
- Show sharable rides result (ride sharer) : http://vcm-12439.vm.duke.edu:8000/DukeDidi/searchSharableRides
  - This page shows all rides that satisfy the sharer's specifications in the previous URL (DukeDidi/searchSharableRides). If there is no such ride available, it will tell the user "No Available Rides!".
- View confirmed rides (ride owner and sharer): http://vcm-12439.vm.duke.edu:8000/DukeDidi/viewConfirmedRides
  - In this page, ride owner and sharer can view their rides that are confirmed by drivers but have not been completed yet.
- View non-completed rides(ride owner and sharer): http://vcm-12439.vm.duke.edu:8000/DukeDidi/viewNonCompletedRides
  - In this page, ride owner and sharer can view any non-complete ride they belong to. This is similar to the previous function (View confirmed rides). The difference is , view non-completed rides can show both open rides and confirmed rides, but view confirmed rides can only show confirmed ride without open rides.
- View open rides and choose one to edit (ride owner and sharer): http://vcm-12439.vm.duke.edu:8000/DukeDidi/viewOpenRides
  - Both ride owner and sharer can view the open rides they belong to. And they can choose one to edit. If a ride owner choose to edit a ride, this ride should have no sharers. If a sharer choose to edit a ride, he/she can just choose to quit the ride or not.
- DashBoard (Main Page) : http://vcm-12439.vm.duke.edu:8000/DukeDidi/dashboard/
  - This page covers all the links to different functionality. User here can "register as a driver", "edit his driver status if he is a driver", "request a ride", "search sharable rides as sharer", "view non-complete rides", "view open rides", "go to driver dashboard", "view confirmed rides", "log out". Any illegal operations will lead to 404, such as trying to edit driver status when he is not a driver yet. 

- Driver DashBoard (Driver Main Page) : http://vcm-12439.vm.duke.edu:8000/DukeDidi/driverDashboard
  -  This page supports two functionality. User here can "search open rides which confirms to driver's status" and "view previous confirmed rides" 
- Driver Search Suitable Open Rides : http://vcm-12439.vm.duke.edu:8000/DukeDidi/driverOpenRides
  - This page shows driver rides that they can pick up, if any suitable rides exist. If there is no available one, "No Available Rides" is printed. If driver want to pick up one ride, he can choose that radio button and click "pick order". The driver can also click bottom link to back to Driver DashBoard, if he do not want to pick order.
- Driver Pick Up One Ride : http://vcm-12439.vm.duke.edu:8000/DukeDidi/driverSelectRides
  - After choosing ride to pick, the driver will get into this page, which shows he has picked successfully and inform him to pickup passengers. Also, once the driver confirms one ride, passengers will receive emails notification.
- Register as Driver : http://vcm-12439.vm.duke.edu:8000/DukeDidi/driverRegister/
  - If a user want to become a driver, he can click the button in dashboard. In this page, user is required to fill information about his vehicle capacity and his license plate number. If any wrong information is filled or some fields are not filled, the page will show "Illegal capacity or license plate number!". If a user is already a driver, the page will show "You are already a driver".
- Driver View Confirmed Ride & Choose to Complete : http://vcm-12439.vm.duke.edu:8000/DukeDidi/driverViewConfirmedRides
  -  This page shows driver all confirmed rides that he pick up, he can choose one to mark it as complete, meaning he has finished deliver passengers of this ride. He can also back to driver dashboard by click on link.
- Edit Driver Status : http://vcm-12439.vm.duke.edu:8000/DukeDidi/editDriver/
  - This page allows driver to edit his vehicle information and type.  If any wrong information is filled or some fields are not filled, the page will show "Illegal capacity or license plate number!". If a user is not driver yet and click this button, the error messege will also appear.
- Edit Open Ride : http://vcm-12439.vm.duke.edu:8000/DukeDidi/editOpenRide
  - After user view their open rides, they can choose one to edit. If an user is an owner, he can only edit his open ride when there is no sharer. If an user is a sharer, he can not edit detail of open ride, but can cancel this open ride.











