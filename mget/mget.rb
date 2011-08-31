require 'rubygems'
require 'httpclient'

URL_FORMATS=[
["%simage/%02d_%02x.jpg", "%s%02d_%02x.html"],
["%simage/%03d_%02x.jpg", "%s%03d_%02x.html"]
]

SAVE_DIR = "/Users/makiton/mogumogu/%s"

def download_images(base_url)
    c = HTTPClient.new(:agent_name => "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6")

    save_dir = SAVE_DIR % base_url+"image"
    unless File.exist?(save_dir)
        FileUtils.makedirs(save_dir)
    end
    page = 0
    url_type = 0
    loop do
        break unless URL_FORMATS[url_type]
        image_url = URL_FORMATS[url_type][0] % [base_url, page, page]
        print image_url + "\n"
        referer = URL_FORMATS[url_type][1] % [base_url, page, page]

        filename = SAVE_DIR % image_url
        print filename+"\n"
        if File.exist?(filename)
            page += 1
            next
        end

        ret = c.get(image_url, nil, {'Referer'=>referer})
        # trying other url type 
        if (ret.status != 200) and page == 0
            url_type += 1
            next
        end
        # probably finished downloads
        break if ret.status == 404
        # probably redirect due to bad request
        if ret.status != 200
            print "bad request?"
            break
        end

        file = File.open(filename, "wb")
        file.write(ret.content)
        file.close

        page += 1
        break if page>150
    end
end

ARGV.each do |u|
    download_images(u)
end

