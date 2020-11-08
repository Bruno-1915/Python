
  INTEGER, PARAMETER                      ::  PREC = SELECTED_REAL_KIND(9,99)
  REAL(PREC), DIMENSION(:), ALLOCATABLE   ::  psi
  REAL(PREC)                              ::  dx,V,e_guess,de
  n=1050 
  ALLOCATE (psi(-n-3:n))

  call inicializa(psi,n,dx,V,e_guess,de)
  call calcula_sinNumerov(psi,n,dx,V,e_guess,de)
  call system('gnuplot script.gnp')
END PROGRAM 

SUBROUTINE inicializa(psi, n, dx, V, e_guess, de)
!psi: funcion de onda
!dx es el pasito espacial
!square well corre de -xmax a xmax
!V es el potencial en las paredes del pozo
!e es la energia y de es el paso en la energia
  INTEGER, PARAMETER                      ::  PREC = SELECTED_REAL_KIND(9,99)
  INTEGER, INTENT (IN)                    ::  n
  REAL(PREC), DIMENSION(-n-3:n)             ::  psi
  REAL(PREC)                              ::  dx,V,e_guess,de
  dx = 0.001
  V  = 1000.0
  e_guess  = 2.0
  de = -0.06
END SUBROUTINE inicializa

SUBROUTINE calcula_sinNumerov(psi,n,dx,Vmax,energia,de)
  INTEGER, PARAMETER               ::  PREC = SELECTED_REAL_KIND(9,99)
  INTEGER, INTENT (IN)             ::  n
  REAL(PREC), DIMENSION(-n-3:n)      ::  psi
  REAL(PREC)                       ::  dx,V,energia,de,Vmax
  INTEGER                          ::  i,last_diverge,unidades,decenas,centenas
  INTEGER                          ::  miles,diverge,k,contador,j
  CHARACTER(LEN=4)                 ::  nom !el numero 0000
  CHARACTER(LEN=11)                ::  fpos
  CHARACTER(LEN=19),  PARAMETER    ::  f3   = '(ES18.6,t20,ES18.6)' !el formato del write de cada energy0000
  PI      = 4.*ATAN(1.)
  psi(0)  =1.0
  psi(-1) =1.0
  last_diverge=0
  contador=0
!
OPEN(UNIT=33, FILE='script.gnp', status='unknown')
  DO k=1,100
    print*,' Energia calculada', energia,contador
    DO I = 0,N-1
       psi(i+1) = 2.0*psi(i)-psi(i-1)-2.0*(energia - potencial(i*dx,Vmax))*dx**2*psi(i)! Aqui tenemos un quasiVerlet
     
       if (abs(psi(i)) > 2 ) EXIT !Cuando empieza a diverger, ya sea para arriba o para abajo, deja de de "integrar"
    ENDDO
    DO I = -n,-2, 1
       psi(i) = psi(-i)
    ENDDO
!  Ponerle el nombre a los archivos "energia0000" cada vez que haya empezado a diverger
    contador = contador + 1 !Va avanzando en uno energia0001, 0002, etc
    unidades    = MOD(contador, 10)
    decenas    = MOD(contador - unidades, 100) / 10
    centenas    = MOD(contador - unidades - decenas, 1000) / 100
    miles    = MOD(contador - unidades - decenas - centenas, 10000) / 1000
    nom      = ACHAR(miles + 48) // ACHAR(centenas + 48) // &
                 ACHAR(decenas + 48) // ACHAR(unidades + 48)
    nom      = ADJUSTL(nom)
    fpos     = 'energia' // nom 
!
    OPEN(unit=31, file=fpos, status='unknown')
    DO I=-N,N,1
   !
      WRITE(31,f3) psi(i),i*dx
   !
    ENDDO
    CLOSE(31)
   OPEN(unit=33, file='script.gnp', status= 'unknown')
   write(33,*) 'plot "',fpos,'" u 2:1 w l'
   write(33,*) 'pause .5'

   
!  Nos salimos de la integracion para cambiar la energia y revertirel crecimiento de psi 
    if (psi(1000) > 0 )then ! Si en la pared psi estaba por encima del cero, le falta energia
       diverge = 1
    else
       diverge = -1! Si psi llega por debajo del cero le sobra energia
    endif
!  Ahora vamos a hacer biseccion:
    if ((diverge*last_diverge) < 0) de=-de/2.0 !hay que cortar el paso de la energia de, y a ver si nos volvemos a pasar
       energia = energia + de
       last_diverge = diverge
!    
!
   
  ENDDO
close(33)

END SUBROUTINE calcula_sinNumerov
    
  FUNCTION potencial(x,V) !Solo en paredes V=10e5 dizque muy grande
  INTEGER, PARAMETER               ::  PREC = SELECTED_REAL_KIND(9,99)
  REAL(prec)                       ::  x,V
  If ( abs(x) <= 1) then
     potencial = 0.0
  else
     potencial = V
  end if
  RETURN
  END




