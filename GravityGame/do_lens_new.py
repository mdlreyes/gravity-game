from scipy import misc
import numpy as np
from scipy import interpolate
from scipy import misc
import astropy.cosmology as cosmo
import cmath as c


def reduce_size(inp):

    image = inp 
    t_map = image[:,:,0]
    q_map = image[:,:,1]
    u_map = image[:,:,2]
    
    [m,n] = t_map.shape
    k = min(m,n)
    
    ratio = 1020./k
    
    m_new = int(round(m*ratio))
    n_new = int(round(n*ratio))
    
    t_map = misc.imresize(t_map,(m_new,n_new),interp='bilinear')
    q_map = misc.imresize(q_map,(m_new,n_new),interp='bilinear')
    u_map = misc.imresize(u_map,(m_new,n_new),interp='bilinear')
    
    if n == m:
        
        t_map_n = t_map
        q_map_n = q_map
        u_map_n = u_map
    
    elif n == k and n != m:
        dif = abs(n_new-m_new)
        if dif/2 == round(dif/2):
            t_map_n = t_map[dif/2:dif/2+n_new,:]
            q_map_n = q_map[dif/2:dif/2+n_new,:]
            u_map_n = u_map[dif/2:dif/2+n_new,:]
    
        else:
            t_map_n = t_map[int(dif/2-0.5):(m_new-int(dif/2-0.5)),:]
            q_map_n = q_map[int(dif/2-0.5):(m_new-int(dif/2-0.5)),:]
            u_map_n = u_map[int(dif/2-0.5):(m_new-int(dif/2-0.5)),:] 
                
    elif m == k and n != m:
        dif = abs(m_new-n_new)
        if dif/2 == round(dif/2):
            t_map_n = t_map[:,dif/2:dif/2+m_new]
            q_map_n = q_map[:,dif/2:dif/2+m_new]
            u_map_n = u_map[:,dif/2:dif/2+m_new]
        else:
            t_map_n = t_map[:,int(dif/2+0.5):(n_new-int(dif/2-0.5))]  
            q_map_n = q_map[:,int(dif/2+0.5):(n_new-int(dif/2-0.5))]  
            u_map_n = u_map[:,int(dif/2+0.5):(n_new-int(dif/2-0.5))]  
                
    p = len(t_map_n)
    image_lensed = np.zeros((p,p,3))
    
    image_lensed[:,:,0] = t_map_n
    image_lensed[:,:,1] = q_map_n
    image_lensed[:,:,2] = u_map_n
    
    return image_lensed  
    
def deflection_field(x,y,R,truncation):
    
    if truncation == True:
    
        r = np.sqrt(x**2+y**2)
        c2 = np.log(1.+R)-R/(1.+R)
    
        if 0. < r < R and r != 1:
        
            f = (-2.*c.atan(c.sqrt(R**2-r**2)/c.sqrt(-1.+r**2))/c.sqrt(-1.+r**2)+2.*c.atan(c.sqrt(R**2-r**2)/(R*c.sqrt(-1.+r**2)))/c.sqrt(-1.+r**2)+c.log(R+c.sqrt(R**2-r**2))-c.log(R-c.sqrt(R**2-r**2))-2.*c.sqrt(R**2-r**2)/(1.+R)-2.*(-R+(1.+R)*c.log(1.+R))/(1.+R))/r**2
            f = f.real


        elif r == 0.:
        
            f = 0.
    
        else:
            
            f = -2.*c2/r**2
          
    
        alpha_x = -x*f
        alpha_y = -y*f
        
        
    else:
        
        R = 0.5*R
        r = np.sqrt(x**2+y**2)
        c2 = np.log(1.+R)-R/(1.+R)
    
        if 0. < r < R and r != 1:
        
            f = (-2.*c.atan(c.sqrt(R**2-r**2)/c.sqrt(-1.+r**2))/c.sqrt(-1.+r**2)+2.*c.atan(c.sqrt(R**2-r**2)/(R*c.sqrt(-1.+r**2)))/c.sqrt(-1.+r**2)+c.log(R+c.sqrt(R**2-r**2))-c.log(R-c.sqrt(R**2-r**2))-2.*c.sqrt(R**2-r**2)/(1.+R)-2.*(-R+(1.+R)*c.log(1.+R))/(1.+R))/r**2
            f = f.real


        elif r == 0.:
        
            f = 0.
    
        else:
            
            f = -2.*c2/r**2
          
    
        alpha_x = -x*f
        alpha_y = -y*f        
        
        
    return (alpha_x,alpha_y)     
class nfw_halo:
    
    def __init__(self,r_s,c,z_halo,z_source,nx,dx,cosmology,pos,trunc):
        
        c_light = 299792458.
        G = 6.674*(10.**(-11))
        solar = 1.98855*(10.**30)    #Solar mass in kg
        mpc = 3.08567758149137*(10.**22)   #Mpc in m        

        self.r_s = r_s
        self.c = c
        self.z_halo = z_halo
        self.z_source = z_source
        self.nx = nx
        self.dx = dx
        self.cosmology = cosmology
        self.trunc = trunc

        self.d_l = cosmology.comoving_distance(self.z_halo).value #In Mpc
        self.d_s = cosmology.comoving_distance(self.z_source).value
        self.d_ls = cosmology._comoving_distance_z1z2(self.z_halo, self.z_source).value
        self.dx_physical = self.dx*self.d_l

        self.rho_c = cosmology.critical_density(self.z_halo).value*1000.*mpc**3/solar
        self.rho_0 = self.rho_c*500./3.*self.c**3/(np.log(1.+self.c)-self.c/(1.+self.c))
        self.r_500 = self.c*self.r_s
        self.R= 5.*self.r_500


        c_units = c_light/mpc    #c in Mpc units
        self.gamma = G/c_light**2*solar/mpc  #G/c**2 in Solar mass/Mpc units
        self.M_500 = 500.*4.*np.pi/3.*self.rho_c*self.r_500**3

        self.theta_500 = self.r_s/self.d_l*(self.c*(1.+self.z_halo))
            
        #Direct calculation of the deflection field
            
        self.deflection_x = np.zeros((self.nx,self.nx))
        self.deflection_y = np.zeros((self.nx,self.nx))
        
        self.d_l_ad = self.d_l/(1.+z_halo)
        self.d_s_ad = self.d_s/(1.+z_source)
        self.d_ls_ad = cosmology.angular_diameter_distance_z1z2(self.z_halo,self.z_source).value
        self.Sigma_c = 1./(4.*np.pi*self.d_l_ad*self.d_ls_ad*self.gamma)*self.d_s_ad
        
        if pos == 1:
            a = 1./6.
            b = 1./6.
        elif pos == 2:
            a = 1./2.
            b = 1./6.
        elif pos == 3:
            a = 5./6.
            b = 1./6.
            
        elif pos == 4:
            a = 1./6.
            b = 1./2.
        elif pos == 5:
            a = 1./2.
            b = 1./2.
        elif pos == 6:
            a = 5./6.
            b = 1./2.
        elif pos == 7:
            a = 1./6.
            b = 5./6.
        elif pos == 8:
            a = 1./2.
            b = 5./6.
        elif pos == 9:
            a = 5./6.
            b = 5./6.
    
        a = a*nx
        b = b*nx
        
        for i in range(0,nx,1):
            
            for j in range(0,nx,1):
                
                if self.r_s != 0.:
                
                    y = (i-b)*self.dx*self.d_l_ad/self.r_s
                    x = (j-a)*self.dx*self.d_l_ad/self.r_s
                    (self.deflection_x[i,j],self.deflection_y[i,j]) = deflection_field(x,y,self.R/self.r_s,self.trunc)
                    
                else:
                    
                    deflection_x = np.zeros((nx,nx))
                    deflection_y = np.zeros((nx,nx))
        
        self.deflection_x = self.deflection_x*self.d_ls_ad/self.d_s_ad*8.*np.pi*self.rho_0*self.r_s**2*self.gamma
        self.deflection_y = self.deflection_y*self.d_ls_ad/self.d_s_ad*8.*np.pi*self.rho_0*self.r_s**2*self.gamma



        [self.norm,l] = deflection_field(1.,0.,self.R/self.r_s,self.trunc)
        self.norm = self.norm*self.d_ls_ad/self.d_s_ad*8.*np.pi*self.rho_0*self.r_s**2*self.gamma
        self.deflection_x_normalised = self.deflection_x/self.norm
        self.deflection_y_normalised = self.deflection_y/self.norm

        
    def get_rho_0(self):
        
        return self.rho_0
        
    def get_r_s(self):
        
        return self.r_s

    def get_c(self):
        
        return self.c

    def get_R(self):
        
        return self.R
        
    def get_z_halo(self):
        
        return self.z_halo
        
    def get_z_source(self):
        
        return self.z_source
        
    def get_nx(self):
        
        return self.nx

    def get_dx(self):
        
        return self.dx
        
    def get_cosmology(self):
        
        return self.cosmology
        
    def get_Sigma_c(self):
        
        return self.Sigma_c
        
    def get_M_500(self):
        
        return self.M_500
        
    def get_r_500(self):
        
        return self.r_500
        
    def get_d_l(self):
        
        return self.d_l 
   
    def get_d_s(self):
        
        return self.d_s

    def get_d_ls(self):
        
        return self.d_ls

    def get_gamma(self):
        
        return self.gamma     
        
    def get_norm(self):
        
        return self.norm
        
    def get_deflection_x(self):
        
        return self.deflection_x
        
    def get_deflection_y(self):
        
        return self.deflection_y
        
    def get_deflection_x_norm(self):
        
        return self.deflection_x_normalised
        
    def get_deflection_y_norm(self):
        
        return self.deflection_y_normalised        
            
def grav_lens(input_dir,output_dir):
    
    dis = 2
    pos = 5
    mass = 2
    delens = False
    image = misc.imread(input_dir)
    image = reduce_size(image)
    dx = 0.1/60./180.*np.pi
 #   dx = 0.425/60./180./60.*np.pi
    nx = len(image)
    ny = nx
    dy = dx
    d_source = 20.
    cosmology = cosmo.FlatLambdaCDM(H0=67.26, Om0=0.316)
   
    if dis == 1:    
        z_halo = 0.1  
    elif dis == 2:
        z_halo = 0.5

    
    if mass == 1:
        M = 50.0*10**15
    elif mass == 2:
        M = 200.0*10**15
        
    c = 3.
    solar = 1.98855*(10.**30)    #Solar mass in kg
    mpc = 3.08567758149137*(10.**22)   #Mpc in m     
    rho_c = cosmology.critical_density(0.5).value*1000.*mpc**3/solar
    r_s = (3./4.*M/rho_c/500./np.pi/c**3)**(1./3.)  
        
#    theta_500 = 50
#    d_l = cosmology.comoving_distance(z_halo).value #In Mpc
#    r_s = theta_500/180./60.*np.pi*d_l/(c*(1+z_halo)) #NFW scale radius in Mpc 
    
    halo = nfw_halo(r_s,c,z_halo,1.,nx,dx,cosmology,pos,True)    
    
    t_map = image[:,:,0]
    q_map = image[:,:,1]
    u_map = image[:,:,2]
    
    t_max = np.mean(t_map)
    q_max = np.mean(q_map)
    u_max = np.mean(u_map)
  

       
    alpha_x = halo.get_deflection_x()
    alpha_y = halo.get_deflection_y()
    

    #Lenses CMB map
    

    image_lensed = np.zeros((nx,nx,3))

    x, y   = np.meshgrid( np.arange(0,nx)*dx, np.arange(0,nx)*dx )
    
    lxs    = (x-alpha_x).flatten(); del x
    lys    = (y-alpha_y).flatten(); del y

    t_map_lensed   = interpolate.RectBivariateSpline( np.arange(0,ny)*dy, np.arange(0,nx)*dx, t_map ).ev(lys, lxs).reshape([nx,nx])
    q_map_lensed   = interpolate.RectBivariateSpline( np.arange(0,ny)*dy, np.arange(0,nx)*dx, q_map ).ev(lys, lxs).reshape([nx,nx])
    u_map_lensed   = interpolate.RectBivariateSpline( np.arange(0,ny)*dy, np.arange(0,nx)*dx, u_map ).ev(lys, lxs).reshape([nx,nx])
            
    t_lensed_max = np.mean(t_map_lensed)       
    q_lensed_max = np.mean(q_map_lensed)       
    u_lensed_max = np.mean(u_map_lensed)       
      
    t_map_lensed = t_map_lensed/t_lensed_max*t_max
    q_map_lensed = q_map_lensed/q_lensed_max*q_max
    u_map_lensed = u_map_lensed/u_lensed_max*u_max
    
      
    image_lensed[:,:,0] = t_map_lensed
    image_lensed[:,:,1] = q_map_lensed
    image_lensed[:,:,2] = u_map_lensed

                
    misc.imsave(output_dir,image_lensed)
