Program Pedestrian_Escape_Dynamics
    IMPLICIT NONE
    integer, parameter :: bigreal = SELECTED_REAL_KIND(R=1200)
    real, PARAMETER:: A = 2000.0, B = 0.08, vi_0 = 0.8, m = 80.0, K = 120000.0, kappa = 240000.0, tau = 0.5
    integer::i,j,l,N=50
    real :: x, y, v, door_x, door_y_min, door_y_max, doorwidth=1.0,roomwidth=30.0
    ! real :: fiduetoj_x, fiduetoj_y, fiduetoW_x, fiduetoW_y, n_ijx, n_ijy, n_iW, radius, dij, rij, gx
    real :: xval(1000), yval(1000), vel(1000), xdir(1000), ydir(1000), fiw(1000), shoulderwidth(1000), radius
    real(KIND=bigreal) :: fiduetoj_x, fiduetoj_y, fiduetoW_x, fiduetoW_y, n_ijx, n_ijy, n_iW, dij, rij, gx, fij(1000)
    real :: tmax=5.0, dt=0.01, t=0.0, xx, yy, vvx, vvy

    ! Setting Door parameters
    door_x = roomwidth
    door_y_min = REAL(roomwidth)/2 - (doorwidth)/2
    door_y_max = REAL(roomwidth)/2 + (doorwidth)/2
    
    ! print *," x, y, v , xdir(i), ydir(i) "
    do i=1,N
        call random_number(x)
        call random_number(y)
        call random_number(v)
        call random_number(radius)
        x = roomwidth*x ! A random number between [0,roomwidth]
        y = roomwidth*y ! A random number between [0,roomwidth]
        radius = 0.2*(radius) + 0.5 ! shoulder radius of a person is in between [0.5,0.7]
        v = vi_0
        xval(i) = x
        yval(i) = y
        xdir(i) = roomwidth-x/sqrt((roomwidth-x)**2 + (roomwidth/2-y)**2)
        ydir(i) = (roomwidth/2-y)/sqrt((roomwidth-x)**2 + (roomwidth/2-y)**2)
        vel(i) = v
        shoulderwidth(i) = radius
        ! print *, x, y, v , xdir(i), ydir(i), shoulderwidth(i)
    end do

    ! Calculating net force on each person due to others
    do i=1,N
        fiduetoj_x=0.0d0
        fiduetoj_y=0.0d0
        rij=0.0
        dij=0.0
        ! process others
        do j=1,N
            if(j /= i) then 
            dij = sqrt((xval(i)-xval(j))**2 + (yval(i)-yval(j))**2)
            n_ijx = (xval(i) - xval(j))/dij
            n_ijy = (yval(i) - yval(j))/dij
            rij = shoulderwidth(i) + shoulderwidth(j)
            if(rij-dij > 0) then
                 gx = rij-dij
            else 
                 gx = 0.0
            end if  
            fiduetoj_x = fiduetoj_x + ((A*EXP((rij-dij)/B) + K*gx))*n_ijx
            fiduetoj_y = fiduetoj_y + ((A*EXP((rij-dij)/B) + K*gx))*n_ijy
            endif
        end do
        fij(i) = sqrt(fiduetoj_x*fiduetoj_x + fiduetoj_y*fiduetoj_y)
        ! print* , fij(i)
    end do

    ! Using Verlet Algo
    do i=1,1
    xx = xval(1)
    yy = yval(1)
    vvx=vel(i)
    vvy=vel(i)
    do while(t.le.tmax)
        t = t + dt
        xx = xx + vvx*xdir(i)*dt
        yy = yy + vvy*ydir(i)*dt
        vvx = vvx - ((1/tau) * (vi_0*(xdir(i)) - vel(i)))*dt
        vvy = vvy - ((1/tau) * (vi_0*(ydir(i)) - vel(i)))*dt
        if(xx .gt. door_x .and. (yy .gt. door_y_min .or. yy .lt. door_y_max)) then
            exit
        endif
        print*, t,xx,yy,vvx, vvy
    end do
    end do

end Program Pedestrian_Escape_Dynamics