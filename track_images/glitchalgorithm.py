from PIL import Image
import io, os, random, logging, numpy as np

class Glitch(object):
    def trigger(self, namefile):
        ''' Main trigger function '''
        imgoriginal = Image.open(namefile).convert('RGBA')
        arrdataimg = np.array(imgoriginal)

        nameofcoloredimg = self.append_random_number_to_filename(namefile) + '_colored_.jpg'
        initial_hue = (180 - random.randint(100, 180))/360.0
        initial_sat = 100.0
        initial_val = 20.0
        initial_rand = random.randint(1, 3)
        ic_color = Image.fromarray(
            self.set_hsv(
                arrdataimg,
                initial_hue,
                initial_sat,
                initial_val,
                initial_rand
            ),
            'RGBA'
        )
        os.chdir(os.getcwd() + '/..')
        os.chdir(os.getcwd() + '/glitched')
        ic_color.save(nameofcoloredimg)

        self.glitch_an_image(nameofcoloredimg)
        os.remove(nameofcoloredimg)

        os.chdir(os.getcwd() + '/..')
        os.chdir(os.getcwd() + '/original')

    def append_random_number_to_filename(self, local_img_file):
        ''' Prevent overwriting of original file '''
        abc = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')
        randname = ''
        for j in range(0,5):
            randname += abc[random.randint(0, len(abc) - 1)]
        return "%s__%s" % (randname,random.randint(100000, 999999))

    # Color methods
    def rgb_to_hsv(self, rgb):
        # Translated from source of colorsys.rgb_to_hsv
        # r,g,b should be a numpy arrays with values between 0 and 255
        # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
        rgb = rgb.astype('float')
        hsv = np.zeros_like(rgb)
        # in case an RGBA array was passed, just copy the A channel
        hsv[..., 3:] = rgb[..., 3:]
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        maxc = np.max(rgb[..., :3], axis=-1)
        minc = np.min(rgb[..., :3], axis=-1)
        hsv[..., 2] = maxc
        mask = maxc != minc
        hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
        rc = np.zeros_like(r)
        gc = np.zeros_like(g)
        bc = np.zeros_like(b)
        rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
        gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
        bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
        hsv[..., 0] = np.select(
            [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
        hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
        return hsv

    def hsv_to_rgb(self, hsv):
        # Translated from source of colorsys.hsv_to_rgb
        # h,s should be a numpy arrays with values between 0.0 and 1.0
        # v should be a numpy array with values between 0.0 and 255.0
        # hsv_to_rgb returns an array of uints between 0 and 255.
        rgb = np.empty_like(hsv)
        rgb[..., 3:] = hsv[..., 3:]
        h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        i = (h * 6.0).astype('uint8')
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
        rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
        rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
        rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
        return rgb.astype('uint8')

    def set_hsv(self, arr, hout, sout, vout, randnum):
        hsv = self.rgb_to_hsv(arr)

        hsv[..., 0] = hout
        hsv[..., 1] = (sout/(vout * randnum))

        rgb = self.hsv_to_rgb(hsv)
        return rgb

    # Glitch function that delegates operation for glitch_an_image()
    def glitch_an_image(self, nameimg):
        imagetoglitch = Image.open(nameimg, 'r')
        bytesofimage = imagetoglitch.tobytes()
        ini,end = self.randompoints(len(bytesofimage))
        newimage = Image.frombytes(
            'RGB',
            (800, 600),
            self.newrawbytes(bytesofimage, ini, end),
            'raw'
        )
        newimage.save(nameimg + '_glitched.jpg')

    def randompoints(self,nbytes):
         ini_n = random.randint(0, nbytes - (nbytes/6))
         end_n = random.randint(ini_n, nbytes - (nbytes/12))
         return ini_n,end_n

    def newrawbytes(self, data, ini, end):
        dataraw = ""
        while len(dataraw) < len(data):
            dataraw += data[ini:end]
        return dataraw
        